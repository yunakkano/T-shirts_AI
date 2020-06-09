from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files import File

from datetime import datetime as dt
from .forms import PhotoForm
from .models import Tshirt
from valuator.models import User
from io import BytesIO
from PIL import Image
import base64
import re
import os


def index(request):
    # template = loader.get_template('valuator/index.html')
    tshirts = Tshirt.objects.order_by('-saved_at')
    context = {'form': PhotoForm(), 'tshirts': tshirts}
    return render(request, 'valuator/index.html', context)
    # return HttpResponse(template.render(context, request))


def tshirt_detail(request, tshirt_id):
    tshirt = get_object_or_404(Tshirt, pk=tshirt_id)
    return render(request, 'valuator/tshirt_detail.html', {'tshirt': tshirt })


def valuate(request):
    if not request.method == 'POST':
        return
        redirect('valuator:index')
    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        raise ValueError("Form invalid")

    tshirt = Tshirt(image=form.cleaned_data['image'])
    image_str = tshirt.image_source()
    imtype = re.search("^data:image/(jpeg|png|gif|jpg);base64,", image_str).group(1)
    image_data = re.sub("^data:image/(jpeg|png|gif|jpg);base64,", "", image_str)
    image_data = base64.b64decode(image_data)
    image_data = BytesIO(image_data)
    im = Image.open(image_data)
    imName = str(dt.now()).replace(" ", "_").replace(":", "") + '.' + imtype
    im.save('media/tmp/' + imName, imtype)
    with open('media/tmp/' + imName, 'rb') as reopen:
        django_file = File(reopen)
        tshirt = Tshirt(image=django_file)
    # Call the method to predict
        predicted, percentage = tshirt.valuate()

    context = {
        'predicted':    predicted,
        'percentage':   percentage,
        'tshirt_name':  str(tshirt.image.name).split('/')[-1],
        'tshirt_data':  image_str,
    }
    return render(request, 'valuator/result.html', context)


def save_result(request):
    if not request.method == 'POST':
        return redirect('index')
    if request.POST['saving'] == 'True':
        with open('media/tmp/' + request.POST['tshirt_name'], 'rb') as reopen:
            django_file = File(reopen)
            django_file.name = django_file.name.replace('media/tmp/','')
            tshirt = Tshirt(
                image=django_file,
                price_range=request.POST['predicted'],
                comment=request.POST['comment'],
                saved_at=dt.now(),
                confidence=request.POST['percentage'],
                user=get_object_or_404(User, pk=2)
                )
            tshirt.save()
        os.remove('media/tmp/' + request.POST['tshirt_name'])
        return redirect('index')
    else:
        os.remove('media/tmp/' + request.POST['tshirt_name'])
        return redirect('valuator:index')
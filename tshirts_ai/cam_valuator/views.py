from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.core.files import File
from valuator.models import Tshirt
from valuator.models import User


from io import BytesIO
from PIL import Image
import base64
import re
import os
from datetime import datetime as dt


def index(request):
    current_user = request.user
    return render(
        request,
        'cam_valuator/index.html',
        {'current_user': current_user}
        )


def cam_valuate(request):
    if not request.method == 'POST':
        return
        redirect('cam_valuator:index')
    image_str = request.POST['image_data']
    image_width = int(request.POST['width'])
    image_height = int(request.POST['height'])
    image_data = re.sub("^data:image/png;base64,", "", image_str)
    image_data = base64.b64decode(image_data)
    image_data = BytesIO(image_data)
    im = Image.open(image_data)
    assert (image_width, image_height,) == im.size
    imName = str(dt.now()).replace(" ", "_").replace(":", "") + '.png'
    im.save('media/tmp/' + imName, "png")

    with open('media/tmp/' + imName, 'rb') as reopen:
        django_file = File(reopen)
        tshirt = Tshirt(image=django_file)
        predicted, percentage = tshirt.valuate()

    context = {
        'predicted':    predicted,
        'percentage':   percentage,
        'tshirt_name':  str(tshirt.image.name).split('/')[-1],
        'tshirt_data':  image_str
    }
    return render(request, 'cam_valuator/result.html', context)


def save_result(request):
    current_user = request.user
    if not request.method == 'POST':
        return redirect('index')
    if request.POST['saving'] == 'True':
        with open('media/tmp/' + request.POST['tshirt_name'], 'rb') as reopen:
            django_file = File(reopen)
            django_file.name = django_file.name.replace('media/tmp/', '')
            tshirt = Tshirt(
                image=django_file,
                price_range=request.POST['predicted'],
                comment=request.POST['comment'],
                saved_at=dt.now(),
                confidence=request.POST['percentage'],
                user=get_object_or_404(User, pk=current_user.id)
                )
            tshirt.save()
        os.remove('media/tmp/' + request.POST['tshirt_name'])
        return redirect('index')
    else:
        os.remove('media/tmp/' + request.POST['tshirt_name'])
        return redirect('cam_valuator:index')

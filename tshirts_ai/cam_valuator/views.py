from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from valuator.forms import PhotoForm
from django.core.files import File
from valuator.models import Tshirt


from io import BytesIO
from PIL import Image
import base64
import re
from datetime import datetime as dt


def index(request):
    # Load Django HTML template: loader.get_template will look in './valuator/templates' folder without direction.
    # valuator/index.html is a subfolder under './valuator/templates' folder
    template = loader.get_template('cam_valuator/index.html')

    # context contains variables to be passed to Django HTML template.
    # 'form' variable in the Django HTML holds information of PhotoForm instance
    context = {'form': PhotoForm()}
    return HttpResponse(template.render(context, request))


def cam_valuate(request):
    # POST request = file upload from upload button
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
    imName = str(dt.now()).replace(" ","_").replace(":","") + '.png'
    im.save('tmp/'+ imName, "png")

    reopen = open('tmp/' + imName, 'rb')
    django_file = File(reopen)
    tshirt = Tshirt(image=django_file)
    #tshirt.image.save(imName, django_file, save=True)
    # Call the method to predict
    predicted, percentage = tshirt.valuate()
    template = loader.get_template('cam_valuator/result.html')
    context = {
        'predicted':    predicted,
        'percentage':   percentage,
        'tshirt_name':  tshirt.image.name,
        'tshirt_data':  image_str,
    }
    return HttpResponse(template.render(context, request))

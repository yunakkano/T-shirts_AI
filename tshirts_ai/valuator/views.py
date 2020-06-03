from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .forms import PhotoForm
from .models import Photo


def index(request):
    # Load Django HTML template: loader.get_template will look in './valuator/templates' folder without direction.
    # valuator/index.html is a subfolder under './valuator/templates' folder
    template = loader.get_template('valuator/index.html')

    # context contains variables to be passed to Django HTML template.
    # 'form' variable in the Django HTML holds information of PhotoForm instance
    context = {'form': PhotoForm()}
    return HttpResponse(template.render(context, request))


def valuator(request):
    # POST request = file upload from upload button
    if not request.method == 'POST':
        return
        redirect('valuator:index')
    # If file upload request comes normally,
    # then create PhotoForm instance with file object.
    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        raise ValueError("Form invalid")

    photo = Photo(image=form.cleaned_data['image'])
    # Call the method to predict
    predicted, percentage = photo.valuator()

    template = loader.get_template('valuator/result.html')
    context = {
        'predicted':predicted,
        'percentage':percentage,
        'photo_name':photo.image.name,
        'photo_data':photo.image_source(),
    }

    return HttpResponse(template.render(context, request))
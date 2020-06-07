from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .forms import PhotoForm
from .models import Tshirt


def index(request):
    # template = loader.get_template('valuator/index.html')
    tshirts = Tshirt.objects.order_by('-saved_at')
    context = {'form': PhotoForm(), 'tshirts': tshirts}
    return render(request, 'valuator/index.html', context)
    # return HttpResponse(template.render(context, request))


def valuate(request):
    # POST request = file upload from upload button
    if not request.method == 'POST':
        return
        redirect('valuator:index')
    # If file upload request comes normally,
    # then create PhotoForm instance with file object.
    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        raise ValueError("Form invalid")

    tshirt = Tshirt(image=form.cleaned_data['image'])
    # Call the method to predict
    predicted, percentage = tshirt.valuate()

    template = loader.get_template('valuator/result.html')
    context = {
        'predicted':    predicted,
        'percentage':   percentage,
        'tshirt_name':  tshirt.image.name,
        'tshirt_data':  tshirt.image_source(),
    }

    return HttpResponse(template.render(context, request))

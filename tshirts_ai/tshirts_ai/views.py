from django.shortcuts import render
from django.shortcuts import get_object_or_404
from valuator.models import Tshirt


def index(request):
    tshirts = Tshirt.objects.order_by('-saved_at')
    context = {'tshirts': tshirts}
    return render(request, 'index.html', context)


def tshirt_detail(request, tshirt_id):
    tshirt = get_object_or_404(Tshirt, pk=tshirt_id)
    return render(request, 'tshirt_detail.html', {'tshirt': tshirt })


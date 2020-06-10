from django.shortcuts import render
from django.shortcuts import get_object_or_404
from valuator.models import Tshirt


def index(request):
    current_user = request.user
    tshirts = Tshirt.objects.all().filter(user_id=current_user.id).order_by('-saved_at')
    context = {'current_user': current_user, 'tshirts': tshirts}
    return render(request, 'top.html', context)


def tshirt_detail(request, tshirt_id):
    current_user = request.user
    tshirt = get_object_or_404(Tshirt, pk=tshirt_id).filter(user_id=current_user.id).order_by('-saved_at')
    return render(request, 'tshirt_detail.html', {'tshirt': tshirt})

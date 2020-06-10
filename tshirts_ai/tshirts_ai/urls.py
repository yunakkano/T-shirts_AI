"""tshirts_ai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth.views import LogoutView
from register import views as v

app_name = 'valuator'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', v.SignUp.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', include("django.contrib.auth.urls")),
    path('valuator/', include('valuator.urls')),
    path('cam_valuator/', include('cam_valuator.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

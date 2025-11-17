"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include # new
from django.views.generic.base import TemplateView # new
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static 
=======
from debug_toolbar.toolbar import debug_toolbar_urls
>>>>>>> 6948120227e20c76cd582081d7fa9a8d01cd5c88

urlpatterns = [
path("admin/", admin.site.urls),
path("accounts/", include("accounts.urls")), # new
path("accounts/", include("django.contrib.auth.urls")), # new
path("", TemplateView.as_view(template_name="home.html"),
name="home"), # new
path("", include("pages.urls")), # new
<<<<<<< HEAD
path('shop/', include('shop.urls')),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
] + debug_toolbar_urls()
>>>>>>> 6948120227e20c76cd582081d7fa9a8d01cd5c88


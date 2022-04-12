"""oddam_w_dobre_rece URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from oddam_w_dobre_rece_app.views import LandingPageView, AddDonationView, LoginView, RegisterView, LogoutView,\
    UserView, get_institution_by_category, activate, FormConfirmationView, EditUserView, EditPasswordView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='index'),
    path('adddonation/', AddDonationView.as_view(), name='adddonation'),
    path('form-confirmation/', FormConfirmationView.as_view(), name='form-confirmation'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserView.as_view(), name='user'),
    path('edit-user/', EditUserView.as_view(), name='edit-user'),
    path('edit-password/', EditPasswordView.as_view(), name='edit-password'),
    path('get_institution_by_category/', get_institution_by_category, name='get_institution_by_category'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
]

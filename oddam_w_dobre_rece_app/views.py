from django.shortcuts import render
from django.views import View

# Create your views here.


class LandingPageView(View):
    """
    Widok LandingPage
    """
    def get(self, request):
        return render(request, 'oddam_w_dobre_rece_app/index.html')


class AddDonationView(View):
    """
    Widok AddDonation
    """
    def get(self, request):
        return render(request, 'oddam_w_dobre_rece_app/form.html')


class LoginView(View):
    """
    Widok Login
    """
    def get(self, request):
        return render(request, 'oddam_w_dobre_rece_app/login.html')


class RegisterView(View):
    """
    Widok Register
    """
    def get(self, request):
        return render(request, 'oddam_w_dobre_rece_app/register.html')

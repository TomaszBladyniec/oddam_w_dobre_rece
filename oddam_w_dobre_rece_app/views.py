from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.template.loader import render_to_string
from .models import Category, Donation, Institution
from .forms import MyUserCreation
from .tokens import account_activation_token
import re

# Create your views here.


class LandingPageView(View):
    """
    Widok LandingPage
    """
    def get(self, request):
        donations = list(Donation.objects.values_list('quantity'))
        no_of_bags = 0
        for i in range(0, len(donations)):
            no_of_bags += donations[i][0]
        no_of_inst = Institution.objects.all().count()
        foundations = Institution.objects.filter(type='1')
        paginator_foundations = Paginator(foundations, 5)  # Show 5 elements per page
        ngos = Institution.objects.filter(type='2')
        paginator_ngos = Paginator(ngos, 5)  # Show 5 elements per page
        fundraisings = Institution.objects.filter(type='3')
        paginator_fundraisings = Paginator(fundraisings, 5)  # Show 5 elements per page
        page = request.GET.get('page')
        foundations = paginator_foundations.get_page(page)
        ngos = paginator_ngos.get_page(page)
        fundraisings = paginator_fundraisings.get_page(page)
        user = request.user
        return render(request, 'oddam_w_dobre_rece_app/index.html', {'no_of_inst': no_of_inst,
                                                                     'no_of_bags': no_of_bags,
                                                                     'foundations': foundations,
                                                                     'ngos': ngos,
                                                                     'fundraisings': fundraisings,
                                                                     'user': user})


class AddDonationView(LoginRequiredMixin, View):
    """
    Widok AddDonation
    """
    def get(self, request):
        category = Category.objects.all()
        institution = Institution.objects.all()
        return render(request, 'oddam_w_dobre_rece_app/form.html', {'category': category, 'institution': institution})


class FormConfirmationView(LoginRequiredMixin, View):
    """
    Widok FormConfirmation
    """
    def post(self, request):
        quantity = request.POST['bags']
        categories = request.POST.getlist('categories')
        institution = request.POST['organization']
        address = request.POST['address']
        phone_number = request.POST['phone']
        city = request.POST['city']
        zip_code = request.POST['postcode']
        pick_up_date = request.POST['data']
        pick_up_time = request.POST['time']
        pick_up_comment = request.POST['more_info']
        donation = Donation.objects.create(
            quantity=quantity,
            institution=Institution.objects.get(id=institution),
            address=address,
            phone_number=phone_number,
            city=city,
            zip_code=zip_code,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=request.user
        )
        donation.categories.set(categories)
        return render(request, 'oddam_w_dobre_rece_app/form-confirmation.html')


class LoginView(View):
    """
    Widok Login
    """
    def get(self, request):
        form = LoginForm()
        return render(request, 'oddam_w_dobre_rece_app/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user = authenticate(username=user_login, password=user_password)
            if user is None:  # zły login albo/i hasło
                return redirect('/register/')
            else:  # user znaleziony, można zalogować
                login(request, user)
                return redirect('/')
        else:
            return redirect('/login/')


class LogoutView(LoginRequiredMixin, View):
    """
    Formularz wylogowania
    """
    def get(self, request):
        logout(request)
        return redirect('/')


class RegisterView(View):
    """
    Widok Register
    """
    def get(self, request):
        form = RegisterForm()
        return render(request, 'oddam_w_dobre_rece_app/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if re.fullmatch(r'[A-Za-z0-9!?@#$%^&+=]{8,}', password):
                user = User.objects.create_user(
                    username=email,
                    first_name=name,
                    last_name=surname,
                    email=email,
                    password=password
                )
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                message = render_to_string('oddam_w_dobre_rece_app/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return redirect('/login/')
            else:
                return HttpResponse('Hasło powinno składać się co najmniej z 8 znaków, zawierać małe, wielkie litery, cyfry i znaki specjalne.')
        else:
            return render(request, 'oddam_w_dobre_rece_app/register.html', {'form': form})


class UserView(LoginRequiredMixin, View):
    """
    Widok User
    """
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user=request.user)
        return render(request, 'oddam_w_dobre_rece_app/user.html', {'user': user, 'donations': donations})


def get_institution_by_category(request):
    category_ids = request.GET.getlist('category_ids')
    if category_ids is not None:
        institutions = Institution.objects.filter(category__in=category_ids).distinct()
    else:
        institutions = Institution.objects.all()
    return render(request, "oddam_w_dobre_rece_app/api_institutions.html", {'institutions': institutions, 'form': MyUserCreation()})
    # return HttpResponse(str(request.GET.getlist("kategorie")))


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Dziękuję za potwierdzenie. Teraz możesz się zalogować.')
    else:
        return HttpResponse('Kod aktywacyjny jest niepoprawny!')
from django.shortcuts import redirect, render
from django.views import View
from .models import Donor
from .forms import LoginForm, UserForm, DonorSignupForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, "index.html")


def gallery(request):
    return render(request, "gallery.html")


def login_admin(request):
    return render(request, "login-admin.html")


class login_donor(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login-donor.html", locals())
    def post(self, request):
        form = LoginForm(request.POST)
        us = request.POST['username']
        pwd = request.POST['password']   
        try:
            user = authenticate(username=us, password=pwd)
            if user:
                donor_user = Donor.objects.filter(user_id=user.id)
                if donor_user:
                    login(request, user)
                    # messages.success(request, "Login Successfully")
                    return redirect("/index-donor")
                else:
                    messages.warning(request, "Invalid Donor User")
            else:
                messages.warning(request, "Invalid username and password")
        except:
            messages.warning(request, "Login Failed")
        return render(request, "login-donor.html", locals())

def login_beneficiary(request):
    return render(request, "login_beneficiary.html")


def login_volunteer(request):
    return render(request, "login-volunteer.html")


class signup_donor(View):
    def get(self, request):
        form1 = UserForm()
        form2 = DonorSignupForm() 
        return render(request, "signup_donor.html", locals())
    def post(self, request):
        form1 = UserForm(request.POST)
        form2 = DonorSignupForm(request.POST,  request.FILES) 
        if form1.is_valid() and form2.is_valid():
            fn = request.POST ["first_name"]
            ln = request.POST ["last_name"]
            em = request.POST ["email"]
            us = request.POST ["username"]
            pwd = request.POST ["password1"]
            contact = request.POST ["contact"]
            userpic = request.FILES ["userpic"]

            try:
                user = User.objects.create_user(
                    first_name=fn,
                    last_name=ln,
                    username=us,
                    email=em,
                    password=pwd
                )

                Donor.objects.create(
                    user=user,
                    contact=contact,
                    userpic=userpic,
                )

                messages.success(request, "Congratulations!! Donor Profile Created Successfully")

            except:
                messages.warning(request, "Profile Not Created")

        return render(request, "signup_donor.html", locals())
  

def signup_volunteer(request):
    return render(request, "signup_volunteer.html")

# ==================================================Donor=================================================
def index_donor(request):
    return render(request, "index-donor.html")


# ==================================================Volunteer=================================================

def index_volunteer(request):
    return render(request, "index-volunteer.html")


# ==================================================Beneficiary=================================================

def index_beneficiary(request):
    return render(request, "index-beneficiary.html")
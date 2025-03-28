from django.shortcuts import redirect, render
from django.views import View
from .models import Beneficiary, Donor, Volunteer
from .forms import BeneficiarySignupForm, LoginForm, UserForm, DonorSignupForm, VolunteerSignupForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, "index.html")


def gallery(request):
    return render(request, "gallery.html")

# ====================================================Login==============================================================
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


class login_beneficiary(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login-beneficiary.html", locals())
    def post(self, request):
        form = LoginForm(request.POST)
        us = request.POST['username']
        pwd = request.POST['password']   
        try:
            user = authenticate(username=us, password=pwd)
            if user:
                beneficiary_user = Beneficiary.objects.filter(user_id=user.id)
                if beneficiary_user:
                    login(request, user)
                    # messages.success(request, "Login Successfully")
                    return redirect("/index-beneficiary")
                else:
                    messages.warning(request, "Invalid Beneficiary User")
            else:
                messages.warning(request, "Invalid username and password")
        except:
            messages.warning(request, "Login Failed")
        return render(request, "login-beneficiary.html", locals())


class login_volunteer(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login-volunteer.html", locals())
    def post(self, request):
        form = LoginForm(request.POST)
        us = request.POST['username']
        pwd = request.POST['password']   
        try:
            user = authenticate(username=us, password=pwd)
            if user:
                volunteer_user = Volunteer.objects.filter(user_id=user.id)
                if volunteer_user:
                    login(request, user)
                    # messages.success(request, "Login Successfully")
                    return redirect("/index-volunteer")
                else:
                    messages.warning(request, "Invalid Volunteer User")
            else:
                messages.warning(request, "Invalid username and password")
        except:
            messages.warning(request, "Login Failed")
        return render(request, "login-volunteer.html", locals())


# ===========================================Signup===========================================

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
  

class signup_volunteer(View):
    # return render(request, "signup_volunteer.html")
    def get(self, request):
        form1 = UserForm()
        form2 = VolunteerSignupForm() 
        return render(request, "signup_volunteer.html", locals())
    def post(self, request):
        form1 = UserForm(request.POST)
        form2 = VolunteerSignupForm(request.POST,  request.FILES) 
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

                Volunteer.objects.create(
                    user=user,
                    contact=contact,
                    userpic=userpic,
                )

                messages.success(request, "Congratulations!! Volunteer Profile Created Successfully")

            except:
                messages.warning(request, "Profile Not Created")

        return render(request, "signup_volunteer.html", locals())

class signup_beneficiary(View):
    def get(self, request):
        form1 = UserForm()
        form2 = BeneficiarySignupForm() 
        return render(request, "signup_beneficiary.html", locals())
    def post(self, request):
        form1 = UserForm(request.POST)
        form2 = BeneficiarySignupForm(request.POST,  request.FILES) 
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

                Beneficiary.objects.create(
                    user=user,
                    contact=contact,
                    userpic=userpic,
                )

                messages.success(request, "Congratulations!! Beneficiary Profile Created Successfully")

            except:
                messages.warning(request, "Profile Not Created")

        return render(request, "signup_beneficiary.html", locals())

# ==================================================Donor=================================================
@login_required(login_url='login_donor')
def index_donor(request):
    try:
        donor = Donor.objects.get(user=request.user)
        return render(request, "index-donor.html", {"donor": donor})
    except Donor.DoesNotExist:
        messages.error(request, "You don't have a donor profile yet.")
        return redirect('login_donor')  


# ==================================================Volunteer=================================================
@login_required(login_url='login_volunteer')
def index_volunteer(request):
    try:
        volunteer = Volunteer.objects.get(user=request.user)
        return render(request, "index-volunteer.html", {"volunteer": volunteer})
    except Volunteer.DoesNotExist:
        messages.error(request, "You don't have a volunteer profile yet.")
        return redirect('login_volunteer')  


# ==================================================Beneficiary=================================================

@login_required(login_url='login_beneficiary')
def index_beneficiary(request):
    try:
        beneficiary = Beneficiary.objects.get(user=request.user)
        return render(request, "index-beneficiary.html", {"beneficiary": beneficiary})
    except Beneficiary.DoesNotExist:
        messages.error(request, "You don't have a beneficiary profile yet.")
        return redirect('login_beneficiary')  




def index_admin(request):
    return render(request, "index-admin.html")


def new_assistance_request(request):
    return render(request, "new-assistance-request.html")

def assistance_request_detail(request):
    return render(request, "assistance-request-detail.html")

def accepted_assistance_request(request):
    return render(request, "accepted-assistance-request.html")

def status_updated_request_detail(request):
    return render(request, "status-updated-request-detail.html")

def rejected_assistance_request(request):
    return render(request, "rejected-assistance-request.html")

def total_volunteer(request):
    return render(request, "total_volunteer.html")

def admin_volunteer_detail(request):
    return render(request, "admin-volunteer-detail.html")
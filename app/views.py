from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    return render(request, "index.html")


def gallery(request):
    return render(request, "gallery.html")


def login_admin(request):
    return render(request, "login-admin.html")


def login_donor(request):
    return render(request, "login-donor.html")


def login_volunteer(request):
    return render(request, "login-volunteer.html")


def signup_donor(request):
    return render(request, "signup_donor.html")


def signup_volunteer(request):
    return render(request, "signup_volunteer.html")



from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("gallery/", views.gallery, name="gallery"),

    path("login-admin/", views.login_admin, name="login_admin"),
    path("index-admin/", views.index_admin, name="index_admin"),

    path("login-volunteer/", views.login_volunteer.as_view(), name="login_volunteer"),
    path("signup-volunteer/", views.signup_volunteer.as_view(), name="signup_volunteer"),
    path("index-volunteer/", views.index_volunteer, name="index_volunteer"),

    path("login-beneficiary/", views.login_beneficiary.as_view(), name="login_beneficiary"),
    path("signup-beneficiary/", views.signup_beneficiary.as_view(), name="signup_beneficiary"),
    path("index-beneficiary/", views.index_beneficiary, name="index_beneficiary"),

    path("login-charity/", views.login_charity_org.as_view(), name="login_charity"),
    path("signup-charity/", views.signup_charity_org.as_view(), name="signup_charity"),
    path("index-charity/", views.index_charity_org, name="index_charity"),


    path("new-assistance-request/", views.new_assistance_request, name="new_assistance_request"),
    path("assistance-request-detail/", views.assistance_request_detail, name="assistance_request_detail"),
    path("accepted-assistance-request/", views.accepted_assistance_request, name="accepted_assistance_request"),
    path("rejected-assistance-request/", views.rejected_assistance_request, name="rejected_assistance_request"),
    path("status-updated-request-detail/", views.status_updated_request_detail, name="status_updated_request_detail"),

    path("total-volunteer/", views.total_volunteer, name="total_volunteer"),
    path("admin-volunteer-detail/", views.admin_volunteer_detail, name="admin_volunteer_detail"),

    path("new-event-request/", views.new_event_request, name="new_event_request"),

]

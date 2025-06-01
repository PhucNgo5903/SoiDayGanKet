
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import views
from app.views import views, admin_views, beneficiary_views,charity_orgs_views, volunteer_views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("gallery/", views.gallery, name="gallery"),

    path("login-admin/", views.login_admin, name="login_admin"),
    path("index-admin/", admin_views.index_admin, name="index_admin"),

    path("login-volunteer/", views.login_volunteer.as_view(), name="login_volunteer"),
    path("signup-volunteer/", views.signup_volunteer.as_view(), name="signup_volunteer"),
    path("volunteer/index-volunteer/", volunteer_views.index_volunteer, name="index_volunteer"),

    path("login-beneficiary/", views.login_beneficiary.as_view(), name="login_beneficiary"),
    path("signup-beneficiary/", views.signup_beneficiary.as_view(), name="signup_beneficiary"),
    path("beneficiary/index-beneficiary/", beneficiary_views.index_beneficiary, name="index_beneficiary"),

    path("login-charity/", views.login_charity_org.as_view(), name="login_charity"),
    path("signup-charity/", views.signup_charity_org.as_view(), name="signup_charity"),
    path("charity-orgs/assistance-requests/", charity_orgs_views.index_charity_org, name="index_charity"),
    path("charity-orgs/assistance-request/<int:pk>/", charity_orgs_views.assistance_request_detail, name="charity_assistance_request_detail"),
    path("charity-orgs/assistance-request/<int:req_id>/create-event/", charity_orgs_views.create_event, name='create_event'),
    path("charity-orgs/profile/", charity_orgs_views.charity_profile_view, name='charity-profile'),
    path("charity-orgs/events/<str:status>/", charity_orgs_views.events_list_by_status, name='charity_events_by_status'),
    path("charity-orgs/event/<int:event_id>/", charity_orgs_views.charity_event_detail, name='charity_event_detail'),
    path("charity-orgs/events/<int:event_id>/completed/", charity_orgs_views.charity_event_completed_detail, name='charity_event_completed_detail'),
    path("charity-orgs/approve-volunteer/<int:registration_id>/", charity_orgs_views.approve_volunteer_registration, name='approve_volunteer_registration'),
    path("charity-orgs/reject-volunteer/<int:registration_id>/", charity_orgs_views.reject_volunteer_registration, name='reject_volunteer_registration'),
    path("charity-orgs/volunteer-reviews/<int:volunteer_id>/", charity_orgs_views.get_volunteer_reviews, name='get_volunteer_reviews'),
    path("charity-orgs/rate-volunteer/", charity_orgs_views.rate_volunteer, name='rate_volunteer'),
    path("charity-orgs/logout/", charity_orgs_views.charity_logout, name='charity_logout'),

    path("new-assistance-request/", admin_views.new_assistance_request, name="new_assistance_request"),
    path("assistance-request-detail/<int:pk>", admin_views.assistance_request_detail, name="assistance_request_detail"),
    path("accepted-assistance-request/", admin_views.accepted_assistance_request, name="accepted_assistance_request"),
    path("rejected-assistance-request/", admin_views.rejected_assistance_request, name="rejected_assistance_request"),
    path("status-updated-request-detail/", admin_views.status_updated_request_detail, name="status_updated_request_detail"),
    

    path("total-volunteer/", admin_views.total_volunteer, name="total_volunteer"),
    path("admin-volunteer-detail/", admin_views.admin_volunteer_detail, name="admin_volunteer_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

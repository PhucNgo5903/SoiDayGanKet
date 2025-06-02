from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import views
from app.views.volunteer_views import volunteer_registered_events
from app.views import views, admin_views, beneficiary_views,charity_orgs_views, volunteer_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("gallery/", views.gallery, name="gallery"),
    path('api/gallery/', views.gallery_api_view, name='gallery_api'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),

    path("login-admin/", views.login_admin, name="login_admin"),
    path("index-admin/", admin_views.index_admin, name="index_admin"),
    path("login-admin/", admin_views.logout, name="admin_logout"),
    #----------------------------------VOLUNTEER----------------------------------------
    path("login-volunteer/", views.login_volunteer.as_view(), name="login_volunteer"),
    path("signup-volunteer/", views.signup_volunteer.as_view(), name="signup_volunteer"),
     path("volunteer/home-volunteer/", volunteer_views.volunteer_home, name="volunteer_home"),
    path("volunteer/event/<int:event_id>/", volunteer_views.event_detail, name="volunteer_event_detail"),
    path("volunteer/events-volunteer/", volunteer_views.volunteer_events, name="volunteer_events"),
    path("volunteer/event/<int:event_id>/register/", volunteer_views.register_event, name="register_event"),
    path('volunteer/registered-events/', volunteer_registered_events, name='volunteer_registered_events'),
    path('volunteer/events/ongoing/', volunteer_views.volunteer_ongoing_events, name='volunteer_ongoing_events'),
    path("volunteer/statistics-volunteer/", volunteer_views.volunteer_statistics, name="volunteer_statistics"),
    path("volunteer/profile-volunteer/", volunteer_views.volunteer_profile, name="volunteer_profile"),
    path("volunteer/logout-volunteer/", volunteer_views.logout_view, name="logout"),


    #--------------------------------- BENEFICIARY-------------------------
    
    path("send-request/", beneficiary_views.send_request, name ="send_request"),
    path("support-status/", beneficiary_views.support_status, name ="support_status"),
    path("login-beneficiary/", views.login_beneficiary.as_view(), name="login_beneficiary"),
    path("signup-beneficiary/", views.signup_beneficiary.as_view(), name="signup_beneficiary"),
    path("beneficiary/index-beneficiary/", beneficiary_views.index_beneficiary, name="index_beneficiary"),
    path('update-status/<int:request_id>/', beneficiary_views.update_user_status, name="update_user_status"),
    path('request/<int:pk>/', beneficiary_views.assistance_request_detail, name="beneficiary_request_detail"),
    path('beneficiary-profile/edit/',  beneficiary_views.edit_beneficiary_profile, name='beneficiary_profile'),
    
    #---------------------------------CHARITY-------------------------
    
    path("login-charity/", views.login_charity_org.as_view(), name="login_charity"),
    path("signup-charity/", views.signup_charity_org.as_view(), name="signup_charity"),
    path("charity-orgs/assistance-requests/", charity_orgs_views.index_charity_org, name="index_charity"),
    path("charity-orgs/assistance-request/<int:pk>/", charity_orgs_views.assistance_request_detail, name="charity_assistance_request_detail"),
    path("charity-orgs/assistance-request/<int:req_id>/create-event/", charity_orgs_views.create_event, name='create_event'),
    path("charity-orgs/profile/", charity_orgs_views.charity_profile_view, name='charity-profile'),
    path("charity-orgs/events/<str:status>/", charity_orgs_views.events_list_by_status, name='charity_events_by_status'),
    path("charity-orgs/event/<int:event_id>/", charity_orgs_views.charity_event_detail, name='charity_event_detail'),
    path("charity-orgs/event/<int:event_id>/completed/", charity_orgs_views.charity_event_completed_detail, name='charity_event_completed_detail'),
    path("charity-orgs/approve-volunteer/<int:registration_id>/", charity_orgs_views.approve_volunteer_registration, name='approve_volunteer_registration'),
    path("charity-orgs/reject-volunteer/<int:registration_id>/", charity_orgs_views.reject_volunteer_registration, name='reject_volunteer_registration'),
    path("charity-orgs/volunteer-reviews/<int:volunteer_id>/", charity_orgs_views.get_volunteer_reviews, name='get_volunteer_reviews'),
    path("charity-orgs/rate-volunteer/", charity_orgs_views.rate_volunteer, name='rate_volunteer'),
    path("charity-orgs/event/<int:event_id>/end/", charity_orgs_views.end_event, name='end_event'),
    path("charity-orgs/logout/", charity_orgs_views.charity_logout, name='charity_logout'),


    path("new-assistance-request/", admin_views.new_assistance_request, name="new_assistance_request"),
    path("assistance-request-detail/<int:pk>", admin_views.assistance_request_detail, name="assistance_request_detail"),
    path("accepted-assistance-request/", admin_views.accepted_assistance_request, name="accepted_assistance_request"),
    path("rejected-assistance-request/", admin_views.rejected_assistance_request, name="rejected_assistance_request"),


    path("new-event-request/", admin_views.new_event_request, name="new_event_request"),
    path("event-detail/<int:event_id>/", admin_views.event_detail, name="event_detail"),
    path("approved-event/", admin_views.approved_event, name="approved_event"),
    path("rejected-event-request/", admin_views.rejected_event_request, name="rejected_event_request"),
    path("full-volunteer-event/", admin_views.full_volunteer_event, name="full_volunteer_event"),
    path("completed-event/", admin_views.completed_event, name="completed_event"),
    path("all-event/", admin_views.all_event, name="all_event"),
    path("admin-beneficiary-detail/<int:user_id>/", admin_views.admin_beneficiary_detail, name="admin_beneficiary_detail"), 
    path("total-beneficiary/", admin_views.total_beneficiary, name="total_beneficiary"),

    path("total-volunteer/", admin_views.total_volunteer, name="total_volunteer"),
    path("admin-volunteer-detail/<int:pk>", admin_views.admin_volunteer_detail, name="admin_volunteer_detail"),

    path("total-charity-orgs/", admin_views.total_charity_orgs, name="total_charity_orgs"),
    path("admin-charity-org-detail/<int:pk>", admin_views.admin_charity_org_detail, name="admin_charity_org_detail"),
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
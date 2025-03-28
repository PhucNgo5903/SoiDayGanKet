from django.contrib import admin
from .models import Beneficiary, Donor, Volunteer
# Register your models here.

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'contact', 'regdate')



@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'contact', 'regdate')



@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'contact', 'regdate')
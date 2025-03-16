from django.contrib import admin
from .models import Donor
# Register your models here.

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'contact', 'regdate')
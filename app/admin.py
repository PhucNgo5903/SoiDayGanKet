# from django.contrib import admin
# from .models import (
#     NguoiDung, Volunteer, Beneficiary, CharityOrg,
#     Skill, VolunteerSkill, SupportArea, SkillsSupportArea,
#     CharityOrgSupportArea, AssistanceRequestType, AssistanceRequestTypeMap,
#     AssistanceRequest, Event, EventRegistration
# )

# @admin.register(NguoiDung)
# class NguoiDungAdmin(admin.ModelAdmin):
#     list_display = ('user', 'role', 'email', 'status', 'created_at')  # Sử dụng 'user' để hiển thị tên người dùng
#     search_fields = ('user__username', 'email')  # Tìm kiếm theo tên người dùng và email
#     list_filter = ('role', 'status')

# @admin.register(Volunteer)
# class VolunteerAdmin(admin.ModelAdmin):
#     list_display = ('user', 'get_username', 'gender')

#     def get_username(self, obj):
#         return obj.user.user.username  # Truy cập tên người dùng từ liên kết 'NguoiDung'
#     get_username.short_description = 'Username'

# @admin.register(Beneficiary)
# class BeneficiaryAdmin(admin.ModelAdmin):
#     list_display = ('user', 'get_username', 'gender')

#     def get_username(self, obj):
#         return obj.user.user.username  # Truy cập tên người dùng từ liên kết 'NguoiDung'
#     get_username.short_description = 'Username'

# @admin.register(CharityOrg)
# class CharityOrgAdmin(admin.ModelAdmin):
#     list_display = ('user', 'get_username', 'type', 'website')

#     def get_username(self, obj):
#         return obj.user.user.username  # Truy cập tên người dùng từ liên kết 'NguoiDung'
#     get_username.short_description = 'Username'

# @admin.register(Skill)
# class SkillAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')

# @admin.register(VolunteerSkill)
# class VolunteerSkillAdmin(admin.ModelAdmin):
#     list_display = ('volunteer', 'skill')

# @admin.register(SupportArea)
# class SupportAreaAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')

# @admin.register(SkillsSupportArea)
# class SkillsSupportAreaAdmin(admin.ModelAdmin):
#     list_display = ('skill', 'support_area')

# @admin.register(CharityOrgSupportArea)
# class CharityOrgSupportAreaAdmin(admin.ModelAdmin):
#     list_display = ('charity_org', 'support_area')

# @admin.register(AssistanceRequestType)
# class AssistanceRequestTypeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')

# @admin.register(AssistanceRequestTypeMap)
# class AssistanceRequestTypeMapAdmin(admin.ModelAdmin):
#     list_display = ('assistance_request', 'type')

# @admin.register(AssistanceRequest)
# class AssistanceRequestAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'beneficiary', 'charity_org', 'title', 'priority',
#         'status', 'created_at'
#     )
#     list_filter = ('priority', 'status')

#     def get_recieve(self, obj):
#         return obj.receive  # Sửa từ 'recieve' thành 'receive' nếu đây là trường hợp hợp lệ trong mô hình
#     get_recieve.short_description = 'Receive'

# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'charity_org', 'title', 'start_time', 'end_time',
#         'status', 'volunteers_number', 'confirmed_by'
#     )
#     list_filter = ('status',)

# @admin.register(EventRegistration)
# class EventRegistrationAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'event', 'volunteer', 'status',
#         'registered_at', 'checked_in_at', 'checked_out_at', 'rating'
#     )
#     list_filter = ('status',)
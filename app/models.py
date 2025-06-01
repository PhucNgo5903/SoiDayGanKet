
from django.db import models
from django.contrib.auth.models import User

# ==== NguoiDung Model ====
class NguoiDung(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('volunteer', 'Volunteer'),
        ('charity', 'Charity Org'),
        ('beneficiary', 'Beneficiary')
    ]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    dob = models.DateField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar_url = models.URLField(
        default='https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg'
    )

    def __str__(self):
        return self.user.username


# ==== Volunteer Model ====
class Volunteer(models.Model):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    user = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')

    def __str__(self):
        return f"{self.user.user.username} (Volunteer)"


# ==== Beneficiary Model ====
class Beneficiary(models.Model):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    user = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')

    def __str__(self):
        return f"{self.user.user.username} (Beneficiary)"


# ==== Charity Organization Model ====
class CharityOrg(models.Model):
    ORG_TYPE_CHOICES = [('local', 'Local'), ('national', 'National'), ('international', 'International')]
    user = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, primary_key=True)
    type = models.CharField(max_length=50, choices=ORG_TYPE_CHOICES)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.user.username} (Charity Org)"


# ==== Skill Model ====
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ==== Volunteer Skill Model ====
class VolunteerSkill(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.volunteer.user.user.username} - {self.skill.name}"


# ==== Assistance Request Type Model ====
class AssistanceRequestType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ==== Skill - Assistance Request Type Mapping Model ====
class SkillAssistanceRequestType(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    assistance_request_type = models.ForeignKey(AssistanceRequestType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('skill', 'assistance_request_type')

    def __str__(self):
        return f"{self.skill.name} - {self.assistance_request_type.name}"


# ==== Charity Org - Assistance Request Type Mapping Model ====
class CharityOrgAssistanceRequestType(models.Model):
    charity_org = models.ForeignKey(CharityOrg, on_delete=models.CASCADE)
    assistance_request_type = models.ForeignKey(AssistanceRequestType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('charity_org', 'assistance_request_type')

    def __str__(self):
        return f"{self.charity_org.user.user.username} - {self.assistance_request_type.name}"


# ==== Assistance Request Model ====
class AssistanceRequest(models.Model):
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    RECEIVING_CHOICES = [('waiting', 'Waiting'), ('received', 'Received')]

    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
    charity_org = models.ForeignKey(CharityOrg, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    receiving_status = models.CharField(max_length=20, choices=RECEIVING_CHOICES,null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    update_by = models.ForeignKey(NguoiDung, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requests')
    update_status_at = models.DateTimeField(null=True, blank=True)
    place = models.TextField()
    proof_url = models.URLField()
    admin_remark = models.TextField(default="No admin remark")

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        """Tự động xử lý receiving_status theo business logic"""
        # Logic cho bản ghi mới
        if self.pk is None:
            if self.status in ['pending', 'rejected']:
                self.receiving_status = None
            elif self.status == 'approved':
                # Khi tạo mới approved request, mặc định là waiting
                self.receiving_status = 'waiting'
        
        # Logic cho bản ghi đã tồn tại (cập nhật)
        else:
            if self.status in ['pending', 'rejected']:
                self.receiving_status = None
            elif self.status == 'approved':
                # Nếu receiving_status là None và status chuyển thành approved
                if self.receiving_status is None:
                    self.receiving_status = 'waiting'
                    
        super().save(*args, **kwargs)

# ==== Assistance Request Type Map Model ====
class AssistanceRequestTypeMap(models.Model):
    assistance_request = models.ForeignKey(AssistanceRequest, on_delete=models.CASCADE)
    type = models.ForeignKey(AssistanceRequestType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.assistance_request.title} - {self.type.name}"


# ==== Assistance Request Image Model ====
class AssistanceRequestImage(models.Model):
    assistance_request = models.ForeignKey(AssistanceRequest, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

    def __str__(self):
        return self.image_url


# ==== Event Model ====
class Event(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'),  ('completed', 'Completed')]

    charity_org = models.ForeignKey(CharityOrg, on_delete=models.CASCADE)
    assistance_request = models.ForeignKey(AssistanceRequest, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(NguoiDung, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_events')
    approved_at = models.DateTimeField(null=True, blank=True)
    report_url = models.URLField(blank=True, null=True)
    confirmed_by = models.BooleanField(default=False)
    volunteers_number = models.BigIntegerField()
    reason = models.TextField(null=True)
    
    def __str__(self):
        return self.title


# ==== Event Registration Model ====
class EventRegistration(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('completed', 'Completed')]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    registered_at = models.DateTimeField(auto_now_add=True)
    checked_in_at = models.DateTimeField(null=True, blank=True)
    checked_out_at = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Registration for {self.event.title} by {self.volunteer.user.user.username}"

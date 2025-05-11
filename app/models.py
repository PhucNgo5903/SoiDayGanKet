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
    password = models.CharField(max_length=128, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# ==== Volunteer Model ====
class Volunteer(models.Model):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    user = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, primary_key=True)  # Liên kết với NguoiDung
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')

    def __str__(self):
        return f"{self.user.user.username} (Volunteer)"


# ==== Beneficiary Model ====
class Beneficiary(models.Model):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    user = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, primary_key=True)  # Liên kết với NguoiDung
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')

    def __str__(self):
        return f"{self.user.user.username} (Beneficiary)"


# ==== Charity Organization Model ====
class CharityOrg(models.Model):
    ORG_TYPE_CHOICES = [('local', 'Local'), ('national', 'National'), ('international', 'International')]

    user = models.OneToOneField(NguoiDung, on_delete=models.CASCADE, primary_key=True)  # Liên kết với NguoiDung
    type = models.CharField(max_length=50, choices=ORG_TYPE_CHOICES)
    website = models.TextField(blank=True, null=True)

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


# ==== Support Area Model ====
class SupportArea(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


# ==== Skill Support Area Model ====
class SkillsSupportArea(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    support_area = models.ForeignKey(SupportArea, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.skill.name} - {self.support_area.name}"


# ==== Charity Org Support Area Model ====
class CharityOrgSupportArea(models.Model):
    charity_org = models.ForeignKey(CharityOrg, on_delete=models.CASCADE)
    support_area = models.ForeignKey(SupportArea, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.charity_org.user.user.username} - {self.support_area.name}"


# ==== Assistance Request Type Model ====
class AssistanceRequestType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ==== Assistance Request Type Map Model ====
class AssistanceRequestTypeMap(models.Model):
    assistance_request = models.ForeignKey('AssistanceRequest', on_delete=models.CASCADE)
    type = models.ForeignKey(AssistanceRequestType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.assistance_request.title} - {self.type.name}"


# ==== Assistance Request Model ====
class AssistanceRequest(models.Model):
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    RECIEVING_CHOICES = [('waiting', 'Waiting'), ('received', 'Received')]

    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)
    charity_org = models.ForeignKey(CharityOrg, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    start_date = models.BigIntegerField()
    end_date = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    receive = models.CharField(max_length=20, choices=RECIEVING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(NguoiDung, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requests')
    approved_at = models.DateTimeField(null=True, blank=True)
    place = models.TextField()
    proof_url = models.TextField()
    image = models.TextField()

    def __str__(self):
        return self.title


# ==== Event Model ====
class Event(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed')]

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
    report_url = models.TextField(blank=True, null=True)
    confirmed_by = models.BooleanField(default=False)
    volunteers_number = models.BigIntegerField()

    def __str__(self):
        return self.title


# ==== Event Registration Model ====
class EventRegistration(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed')]

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
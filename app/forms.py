
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import NguoiDung, Volunteer, CharityOrg, Beneficiary


# ==== Login Form ====
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


# ==== Base Register Form for NguoiDung ====
class BaseRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = NguoiDung
        fields = ['dob', 'phone', 'address', 'description']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save_user(self, role):
        # Tạo User (tài khoản đăng nhập)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        # Tạo NguoiDung liên kết với User
        nguoidung = NguoiDung.objects.create(
            user=user,
            role=role,
            dob=self.cleaned_data['dob'],
            phone=self.cleaned_data['phone'],
            address=self.cleaned_data['address'],
            description=self.cleaned_data['description'],
            status='active'
        )
        return nguoidung


# ==== Volunteer Register Form ====
class VolunteerRegisterForm(BaseRegisterForm):
    gender = forms.ChoiceField(choices=Volunteer.GENDER_CHOICES)

    def save(self, commit=True):
        nguoidung = self.save_user(role='volunteer')
        volunteer = Volunteer.objects.create(
            user=nguoidung,
            gender=self.cleaned_data['gender']
        )
        return volunteer


# ==== Beneficiary Register Form ====
class BeneficiaryRegisterForm(BaseRegisterForm):
    gender = forms.ChoiceField(choices=Beneficiary.GENDER_CHOICES)

    def save(self, commit=True):
        nguoidung = self.save_user(role='beneficiary')
        beneficiary = Beneficiary.objects.create(
            user=nguoidung,
            gender=self.cleaned_data['gender']
        )
        return beneficiary


# ==== Charity Org Register Form ====
class CharityOrgRegisterForm(BaseRegisterForm):
    type = forms.ChoiceField(choices=CharityOrg.ORG_TYPE_CHOICES)
    website = forms.URLField(required=False)

    def save(self, commit=True):
        nguoidung = self.save_user(role='charity')
        charity_org = CharityOrg.objects.create(
            user=nguoidung,
            type=self.cleaned_data['type'],
            website=self.cleaned_data.get('website', '')
        )
        return charity_org
# ==== Event Register Form ====
class EventRegisterForm(forms.Form):
    full_name = forms.CharField(label="Họ và tên", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    phone = forms.CharField(label="Điện thoại", max_length=20, required=True)
    skill_description = forms.CharField(label="Mô tả kĩ năng", widget=forms.Textarea, required=False)

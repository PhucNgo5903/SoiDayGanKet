
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import AssistanceRequest, NguoiDung, Volunteer, CharityOrg, Beneficiary, AssistanceRequestType, CharityOrgAssistanceRequestType
from django.utils import timezone

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

    
# -------------------------------BENEFICIARY------------------------


class AssistanceRequestForm(forms.ModelForm):
    class Meta:
        model = AssistanceRequest
        fields = ['title', 'description', 'priority', 'start_date', 'end_date', 'place', 'proof_url']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class AssistanceRequestTypeForm(forms.Form):
    types = forms.ModelMultipleChoiceField(
        queryset=AssistanceRequestType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assistance Reques Type"
    )


class AssistanceRequestImageForm(forms.Form):
    image = forms.ImageField(
        required=False,
    )

class BeneficiaryProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Họ', max_length=30, required=False)
    last_name = forms.CharField(label='Tên', max_length=150, required=False)
    email = forms.EmailField(label='Email', required=False)
    
    class Meta:
        model = NguoiDung
        fields = ['dob', 'phone', 'address', 'description']
        labels = {
            'dob': 'Ngày sinh',
            'phone': 'Số điện thoại',
            'address': 'Địa chỉ',
            'description': 'Giới thiệu bản thân',
        }
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Gán giá trị ban đầu từ User nếu có
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        nguoidung = super().save(commit=False)

        # Cập nhật thông tin tài khoản User
        if self.user:
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name = self.cleaned_data.get('last_name', '')
            self.user.email = self.cleaned_data.get('email', '')
            if commit:
                self.user.save()

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        if commit:
            nguoidung.save()
        return nguoidung
# ==== Event Register Form ====
class EventRegisterForm(forms.Form):
    full_name = forms.CharField(label="Họ và tên", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    phone = forms.CharField(label="Điện thoại", max_length=20, required=True)
    skill_description = forms.CharField(label="Mô tả kĩ năng", widget=forms.Textarea, required=False)

    
# -------------------------------BENEFICIARY------------------------


class AssistanceRequestForm(forms.ModelForm):
    class Meta:
        model = AssistanceRequest
        fields = ['title', 'description', 'priority', 'start_date', 'end_date', 'place', 'proof_url']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class AssistanceRequestTypeForm(forms.Form):
    types = forms.ModelMultipleChoiceField(
        queryset=AssistanceRequestType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assistance Reques Type"
    )


class AssistanceRequestImageForm(forms.Form):
    image = forms.ImageField(
        required=False,
    )

class BeneficiaryProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Họ', max_length=30, required=False)
    last_name = forms.CharField(label='Tên', max_length=150, required=False)
    email = forms.EmailField(label='Email', required=False)
    
    class Meta:
        model = NguoiDung
        fields = ['dob', 'phone', 'address', 'description']
        labels = {
            'dob': 'Ngày sinh',
            'phone': 'Số điện thoại',
            'address': 'Địa chỉ',
            'description': 'Giới thiệu bản thân',
        }
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Gán giá trị ban đầu từ User nếu có
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        nguoidung = super().save(commit=False)

        # Cập nhật thông tin tài khoản User
        if self.user:
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name = self.cleaned_data.get('last_name', '')
            self.user.email = self.cleaned_data.get('email', '')
            if commit:
                self.user.save()

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        if commit:
            nguoidung.save()
        return nguoidung
# ==== Event Register Form ====
class EventRegisterForm(forms.Form):
    full_name = forms.CharField(label="Họ và tên", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    phone = forms.CharField(label="Điện thoại", max_length=20, required=True)
    skill_description = forms.CharField(label="Mô tả kĩ năng", widget=forms.Textarea, required=False)

class EventCreationForm(forms.Form):
    volunteers_number = forms.IntegerField(
        label="Volunteers Needed",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'required': True})
    )
    start_time = forms.DateTimeField(
        label="Start Date and Time",
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'required': True
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_time = forms.DateTimeField(
        label="End Date and Time",
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'required': True
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    description = forms.CharField(
        label="Event Description",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Event Description (optional)'
        })
    )

    def __init__(self, *args, **kwargs):
        self.assistance_request = kwargs.pop('assistance_request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        now = timezone.now()

        if not start or not end:
            return

        if start < now:
            self.add_error('start_time', "Start time cannot be in the past.")

        if end <= start:
            self.add_error('end_time', "End time must be after start time.")

        if self.assistance_request:
            if start < self.assistance_request.start_date or end > self.assistance_request.end_date:
                raise forms.ValidationError(
                    f"Time must be within the assistance request period: "
                    f"{self.assistance_request.start_date.strftime('%d/%m/%Y %H:%M')} đến "
                    f"{self.assistance_request.end_date.strftime('%d/%m/%Y %H:%M')}."
                )
                
                
# ==== Charity Org Profile Form ====

class CharityOrgProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    website = forms.URLField(required=False)
    type = forms.ChoiceField(choices=CharityOrg.ORG_TYPE_CHOICES)
    assistance_types = forms.ModelMultipleChoiceField(
        queryset=AssistanceRequestType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CharityOrg
        fields = ['type', 'website']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        nguoidung = user.nguoidung

        self.fields['dob'].initial = nguoidung.dob
        self.fields['address'].initial = nguoidung.address
        self.fields['description'].initial = nguoidung.description

        # Lấy danh sách assistance_types qua model trung gian
        charity = nguoidung.charityorg
        assistance_type_ids = CharityOrgAssistanceRequestType.objects.filter(
            charity_org=charity
        ).values_list('assistance_request_type_id', flat=True)

        self.fields['assistance_types'].initial = assistance_type_ids

    def save(self, commit=True):
        charity = super().save(commit=False)

        if commit:
            charity.save()

            nguoidung = charity.user
            nguoidung.dob = self.cleaned_data['dob']
            nguoidung.address = self.cleaned_data['address']
            nguoidung.description = self.cleaned_data['description']
            nguoidung.save()

            # Cập nhật bảng trung gian
            CharityOrgAssistanceRequestType.objects.filter(charity_org=charity).delete()
            for assistance_type in self.cleaned_data['assistance_types']:
                CharityOrgAssistanceRequestType.objects.create(
                    charity_org=charity,
                    assistance_request_type=assistance_type
                )

        return charity
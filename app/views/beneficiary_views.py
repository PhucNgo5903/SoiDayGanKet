from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import AssistanceRequestTypeMap, AssistanceRequestImage, AssistanceRequest
from .views import role_required
from ..forms import AssistanceRequestForm, AssistanceRequestTypeForm, AssistanceRequestImageForm

@role_required('beneficiary')
def index_beneficiary(request):
    return render(request, 'beneficiary/index-beneficiary.html')


@login_required
# views.py
def send_request(request):
    if request.method == 'POST':
        request_form = AssistanceRequestForm(request.POST)
        type_form = AssistanceRequestTypeForm(request.POST)
        image_form = AssistanceRequestImageForm(request.POST)

        if request_form.is_valid() and type_form.is_valid() and image_form.is_valid():
            # Lưu yêu cầu
            assistance_request = request_form.save(commit=False)
            assistance_request.beneficiary = request.user.beneficiary  # ví dụ như vậy
            assistance_request.status = 'pending'
            assistance_request.receiving_status = 'waiting'
            assistance_request.save()

            # Lưu loại trợ giúp
            for type_item in type_form.cleaned_data['types']:
                AssistanceRequestTypeMap.objects.create(assistance_request=assistance_request, type=type_item)

            # Lưu ảnh
            if image_form.cleaned_data['image_url']:
                AssistanceRequestImage.objects.create(
                    assistance_request=assistance_request,
                    image_url=image_form.cleaned_data['image_url']
                )

            return redirect('beneficiary/send-request.html')  # hoặc chuyển hướng

    else:
        request_form = AssistanceRequestForm()
        type_form = AssistanceRequestTypeForm()
        image_form = AssistanceRequestImageForm()

    return render(request, 'beneficiary/send-request.html', {
        'request_form': request_form,
        'type_form': type_form,
        'image_form': image_form,
    })

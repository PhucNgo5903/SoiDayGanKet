from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .views import role_required
from ..forms import HelpRequestForm

@role_required('beneficiary')
def index_beneficiary(request):
    return render(request, 'beneficiary/index-beneficiary.html')


@role_required('beneficiary')
def send_request(request):
    if request.method == 'POST':
        form = HelpRequestForm(request.POST, request.FILES)
        if form.is_valid():
            # Xử lý dữ liệu ở đây, ví dụ lưu vào DB hoặc làm gì đó
            image = form.cleaned_data.get('image_upload')
            # Bạn có thể xử lý file ở đây nếu cần
            return redirect('beneficiary/index-beneficiary.html')  # Đổi thành URL đúng
    else:
        form = HelpRequestForm()
    
    return render(request, 'beneficiary/send-request.html', {'form': form})
from django.shortcuts import render,redirect
from .forms import CustomUserChangeForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
# Create your views here.

## 시리얼키 등록
@login_required
@require_http_methods(['GET','POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('record:main')
    else:
        form = CustomUserChangeForm(instance=request.user)
        context = {
    	'form':form,
    }
    
    return render(request, 'accounts/update.html', context)
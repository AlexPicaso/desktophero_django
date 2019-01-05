from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required(login_url='/accounts/login/')
def head_view(request):
    if request.user.email.lower() not in settings.BETA_USERS:
        return render(request, 'not_allowed.html', {
            'email': request.user.email
        })
    return render(request, 'head.html')

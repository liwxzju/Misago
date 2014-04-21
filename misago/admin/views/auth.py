from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from misago.admin import auth
from misago.users.forms.auth import AdminAuthenticationForm


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request):
    if request.admin_namespace == 'misago:admin':
        target = 'misago'
    elif request.admin_namespace == 'admin':
        target = 'django'
    else:
        target = 'unknown'

    form = AdminAuthenticationForm(request)

    if request.method == 'POST':
        form = AdminAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.user_cache)
            return redirect('%s:index' % request.admin_namespace)

    return render(request, 'misago/admin/login.html',
                  {'form': form, 'target': target})
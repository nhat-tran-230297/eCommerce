from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from order.models import Order

from .forms import AccountEditForm, RegistrationForm
from .models import UserBase
from .tokens import account_activation_token

# Create your views here.

@login_required
def account_dashboard(request):
    """
    Dashboard view (list of completed orders)
    """

    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id, billing_status=True)

    return render(request, 'account/user/dashboard.html', {'orders': orders})

@login_required
def account_edit(request):
    """
    Update/Modify account view
    """

    if request.method == 'POST':
        edit_form = AccountEditForm(instance=request.user, data=request.POST)
        if edit_form.is_valid():
            edit_form.save()

    else:
        edit_form = AccountEditForm(instance=request.user)

    return render(request, 'account/user/edit.html', {'edit_form': edit_form})
    

@login_required
def account_delete(request):
    """ 
    Delete account view
    """

    user = UserBase.objects.get(pk=request.user.pk)
    user.is_active = False
    user.save()
    logout(request)

    return redirect('account:delete_confirm')


def account_register(request):
    """
    Account register view
    """

    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():

            # return a model object user, then add extra data and save it.
            user = register_form.save(commit=False)  # not save yet
            # user.email = register_form.cleaned_data['email']
            user.set_password(register_form.cleaned_data['password'])
            user.is_active = False
            user.save()

            # Setup email
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            protocol = 'https' if request.is_secure() else 'http'
            message = render_to_string('account/registration/account_activation_email.html', {
                'protocol': protocol,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject=subject, message=message, email=user.email)

            return render(request, 'account/registration/account_activation_complete.html')

    else:
        register_form = RegistrationForm()
    
    return render(request, 'account/registration/register.html', {'form': register_form})


def account_activate(request, uidb64, token):
    """
    Account activation
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        return redirect('account:dashboard')
    else:
        return render(request, 'account/register/account_activation_invalid.html')

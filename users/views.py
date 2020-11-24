from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm,UserProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            messages.success(request,'We have sent you an email, please confirm your email address to complete registration')
            email.send()
            # username = form.cleaned_data.get('username')
            # messages.success(request,'We have sent you an email, please confirm your email address to complete registration')
            # messages.success(request,f'Account created. Please Login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, ('Your account have been confirmed.'))
        return redirect('home')
    else:
        messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
        return redirect('login')

@login_required
def profile_page(request):
    if request.method=="POST":
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = UserProfileUpdateForm(data=request.POST,files=request.FILES,instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f"Your account has been updated")
            return redirect('profile_page')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.userprofile)
    
    form_context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/profilepage.html',context=form_context)

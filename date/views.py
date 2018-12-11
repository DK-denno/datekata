from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import EmailMessage
from django.http import HttpResponse
import requests


@login_required
def home(request):
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        profile = Profile(user=request.user)
        profile.save()
    return render(request, 'core/home.html')


@login_required
def profile(request):
    form = ProfileForm()
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            message = 'Fill in the form appropriately'
            return render(request, 'profile/profile.html', {"profile": profile, "form": form, "message": message})
    return render(request, 'profile/profile.html', {"form": form, "profile": profile})


@login_required
def profiles(request, id):
    user = User.objects.get(id=id)
    posts = Posts.objects.filter(user=user)
    return render(request, 'profile/profiles.html', {"user": user, "posts": posts})


@login_required
def about(request):
    response = requests.get('https://www.codewars.com/api/v1/code-challenges/fibonacci')
    kata = response.json()
    return render(request, 'core/about.html', {'des': kata['description'], 'name': kata['name']})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your datekata account.'
            message = render_to_string('registration/active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponse(
            'Thank you for your email confirmation. Now you can' '<a href="/accounts/login"> login </a>your account.')
    else:
        return HttpResponse('Activation link is invalid!')


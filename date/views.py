from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .forms import ProfileForm,MessageForm
from .models import Profile,Messages
from django.contrib.auth.models import User
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
        current_user=request.user
        profile = Profile.objects.get(user=current_user)
        if request.method == 'POST':
                form = ProfileForm(request.POST,request.FILES,instance=profile)
                if form.is_valid():
                        form.save()
                        return redirect('profile')
                else:
                        message = 'Fill in the form appropriately'
                        return render(request,'profile/profile.html',{"profile":profile,"form":form,"message":message})
        return render(request,'profile/profile.html',{"form":form,"profile":profile})

@login_required
def profiles(request,id):
        user=User.objects.get(id=id)
        posts = Posts.objects.filter(user=user)
        return render(request,'profile/profiles.html',{"user":user,"posts":posts})


def message(request,pk):
        recipient = User.objects.get(id=pk)
        messageform = MessageForm()
        messages = Messages.objects.filter(recipient=recipient)
        mess = []
        for message in messages:
                if message.sender == request.user:
                        mess.append(message)
                        print(message.sender)
                        # print (message.recipient)
        if request.method == 'POST':
                messageform = MessageForm(request.POST,request.FILES)
                if messageform.is_valid():
                        messaging = messageform.save(commit=False)
                        messaging.sender = request.user
                        messaging.recipient = recipient
                        messaging.save()
                        return redirect('/')
        return render(request,'chat.html',{"mess":mess,"form":messageform})
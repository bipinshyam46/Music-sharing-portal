
from sqlite3 import IntegrityError
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def about(request):
    return render(request,'home.html')

def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        re_password=request.POST['re_password']

        try:
            if password==re_password:
                User.objects.create_user(username=username,email=email,password=password)
                return redirect(loginuser)
        except IntegrityError:
            pass

    else:
        return render(request,'signup.html')

def userprofile(request):
    email=request.user.email
    public_uploads=Musiclist.objects.filter(status='public')
    private_uploads=Musiclist.objects.filter(access=email)
    protected_uploads=Musiclist.objects.filter(status='protected')
    user_music=[]
    for i in protected_uploads:
        if email in i.access:
            user_music.append(i)
    music_list={'public_uploads':public_uploads,'private_uploads':private_uploads,'user_music':user_music}
    return render(request,'userprofile.html',{'music_list':music_list})

def loginuser(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=authenticate(request,username=email,password=password)
        print(user)
        if user is not None:
            login(request,user)
            request.session['user_id']=user.id

            return redirect(userprofile)
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')

@login_required(login_url='loginuser')
def uploadmusic(request):
    return render(request,'uploadmusic.html')

@login_required(login_url='loginuser')
def upload_public(request):
    if request.method=='POST':
        audio_file=request.FILES.get('audio_file')
        title=request.POST['title']
        artist=request.POST['artist']
        new_file=Musiclist.objects.create(audio_file=audio_file,title=title,artist=artist)
        new_file.save()
        return redirect(uploadmusic)
    else:
        return render(request,'upload.html')

@login_required(login_url='loginuser')
def upload_private(request):
    if request.method=='POST':
        email=request.user.email
        audio_file=request.FILES.get('audio_file')
        title=request.POST['title']
        artist=request.POST['artist']
        status='private'
        new_file=Musiclist.objects.create(audio_file=audio_file,title=title,artist=artist,status=status,access=email)
        new_file.save()
        return redirect(uploadmusic)
    else:
        return render(request,'upload.html')

@login_required(login_url='loginuser')
def upload_protected(request):
    if request.method=='POST':
        audio_file=request.FILES.get('audio_file')
        title=request.POST['title']
        artist=request.POST['artist']
        email=request.POST['email']
        status='protected'
        email_list=email.split(',')
        users=User.objects.all()
        
        reg_emails=[]
        for i in users:
            reg=i.email
            reg_emails.append(i)
        for i in email_list:
            for j in reg_emails:
                if i==str(j):
                    new_file=Musiclist.objects.create(audio_file=audio_file,title=title,artist=artist,status=status,access=i)
                    new_file.save()
                    
        return redirect(uploadmusic)
    else:
        return render(request,'upload_protected.html')

@login_required(login_url='loginuser')
def logoutuser(request):
    logout(request)
    request.session.flush()
    return redirect(about)



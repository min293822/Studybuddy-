from django.shortcuts import render, redirect
from .models import Messages, Room, Topics, User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RoomForm, MyUserCreationForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count

def activity_view(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  messages_form = Messages.objects.filter(
    Q(room__name__icontains=q) |
    Q(user__username__icontains=q) |
    Q(body__icontains=q)
    )[:100]
  context ={
    'messages_form':messages_form
  }
  return render(request, 'activity.html', context)

def topic_view(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  topics = Topics.objects.annotate(room_count=Count('room')).filter(
    Q(name__icontains=q)
    )
  all_topic = sum([item.room_count for item in topics])
  for topic in topics:
    if topic.room_count == 0:
      topic.delete()
      
  context ={
    'all_topic':all_topic,
    'topics':topics,
  }
  return render(request, 'topic.html', context)

def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(description__icontains=q) |
    Q(name__icontains=q) |
    Q(host__username__icontains=q)
    )
  
  topics = Topics.objects.all()[0:rooms.count() * 3]
  
  messages_form = Messages.objects.filter(
    Q(room__name__icontains=q) |
    Q(user__username__icontains=q) |
    Q(body__icontains=q)
    )[0:rooms.count()]
  context = {
    'topics':topics,
    'rooms':rooms,
    'messages_form':messages_form
  }
  return render(request, 'home.html', context)

def editUser(request, pk):
  user = User.objects.get(id=pk)
  form = UserEditForm(initial={
    'name': user.name,
    'email': user.email,
    'bio': user.bio,
    'avatar':user.avatar
  })
  if request.method == "POST":
    user.name = request.POST.get('name')
    user.email = request.POST.get('email')
    user.bio = request.POST.get('bio')
    user.avatar = 'avatar.svg' if request.POST.get('avatar') == '' else request.POST.get('avatar')
      
    user.save()
    messages.success(request, 'Update Successfully!')
    return redirect('home')
  
  context = {
    'form':form,
    'user':user
  }
  return render(request, 'edit-user.html', context)

def userInfo(request, pk):
  user = User.objects.get(id=pk)
  rooms = Room.objects.filter(host=user)
  messages_form = Messages.objects.filter(user=user)
  topics = Topics.objects.all()
  context = {
   'user':user,
   'rooms':rooms,
   'messages_form':messages_form,
   'topics':topics,
  }
  return render(request, 'userInfo.html', context)

def roomDetails(request, pk):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  messages_form = Messages.objects.filter(
    Q(room__name__icontains=q) |
    Q(user__username__icontains=q) |
    Q(body__icontains=q)
    )
  room = Room.objects.get(id=pk)
  messa = room.messages.all()
  participants = room.participants.all()
  url = ''
  if request.method == 'POST':
    if request.user.is_authenticated:
      url = request.POST.get('comment')
      #print(url)
      body = request.POST['comment']
      createMessage = Messages.objects.create(room=room, user=request.user, body=body)
      createMessage.save()
      if request.user not in room.participants.all():
        room.participants.add(request.user)
      url = ''
    else:
      return redirect('login')
  context = {
    'participants':participants,
    'room':room,
    'messa':messa,
    'messages_form':messages_form
  }  
  return render(request, 'room_details.html', context)

def update_room(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(initial={
            'topic': room.topic.name,
            'name': room.name,
            'description': room.description,
        })
  topics = Topics.objects.all()
  if request.method == "POST":
    topic_name = request.POST.get('topic')
    topic, created = Topics.objects.get_or_create(name=topic_name)
    room.topic = topic
    room.name = request.POST.get('name')
    room.description = request.POST.get('description')
    room.save()
    messages.success(request, 'updated Successfully')
    return redirect('home')
  context={
    'form':form,
    'topics':topics
  }
  return render(request, 'room-update.html', context)

@login_required(login_url='login')
def room_form(request):
  form = RoomForm()
  topics = Topics.objects.all()
  if request.method == 'POST':
    topic_name = request.POST.get('topic')
    topic, created = Topics.objects.get_or_create(name=topic_name)
    Room.objects.create(
      topic=topic, 
      host=request.user, 
      name=request.POST.get('name'),
      description=request.POST.get('description')
      )
    messages.success(request, 'room created Successfully')
    return redirect('home')
    
  
  context ={
      "form":form,
      "topics":topics
    }
  return render(request, 'room-create.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
  try:
    room = Room.objects.get(id=pk)
  except ObjectDoesNotExist:
    return HttpResponse('Room does not exist', status=404)
  
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, 'delete.html', {'room':room})

@login_required(login_url='login')
def delete_message(request, pk):
  try:
    message = Messages.objects.get(id=pk)
  except ObjectDoesNotExist:
    return HttpResponse('Message does not exist', status=404)
    
  if request.method == 'POST':
    message.delete()
    return redirect('home')
  return render(request, 'delete.html', {'message':message})

def login_view(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, 'Login Successfully ')
      return redirect('home')
    else:
      messages.error(request, 'Email or password wrong.')
  return render(request, 'login.html')  
    
def signup_view(request):
  form = MyUserCreationForm()
  if request.method == 'POST':
    form = MyUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.save()
      login(request, user)
      messages.success(request, ' Registered Successfully.')
      return redirect('home')
    else:
      messages.error(request, 'An error occur.')
  return render(request, 'signup.html', {'form': form})

@login_required(login_url='login')
def logout_view(request):
  logout(request)
  messages.success(request, 'logout Successfully')
  return redirect('home')
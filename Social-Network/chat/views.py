from django.shortcuts import render, redirect
from chat.models import Room, Messenge
from django.http import HttpResponse, JsonResponse
from profiles.models import Profile
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    listuser = User.objects.all()
    listProfile = Profile.objects.all()
    context={
        "lsUser":listuser,
        "lsProfile":listProfile
    }
    return render(request, 'main/homeMessage.html',context)

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'main/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    room_user_send = request.POST['room_user_send']

    rom_id =str(int(room)+1)+"+"+str(room_user_send)
    rom_id_replace =str(room_user_send)+"+"+str(int(room)+1)
    
    print(rom_id)
    print(type(room))
    print(type(rom_id))
    if Room.objects.filter(name=rom_id).exists() :
        return redirect('/chat/'+rom_id+'/?username='+username)
    elif Room.objects.filter(name=rom_id_replace).exists():
        return redirect('/chat/'+rom_id_replace+'/?username='+username)
    else:
        new_room = Room.objects.create(name=rom_id)
        new_room.save()
        return redirect('/chat/'+rom_id+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    

    User_id = Profile.objects.get(user=request.user)
    nameuser  = str(User_id).split('-')[0]
    imgUrl=User_id.avatar.url
    new_message = Messenge.objects.create(value=message, user=User_id, room=room_id, nameuser= nameuser, imgUrl= imgUrl)
    new_message.save()
    context ={
        "message": message,
        "username": username,
        "room_id" : room_id
    }
    return HttpResponse("successfully")

def getMessages(request, room):
    room_details = Room.objects.get(name= room)
    messages = Messenge.objects.filter(room=room_details.id)
    user =Profile.objects.get(user=request.user)
    user_id = int(request.user.id)+1
    return JsonResponse({"messages":list(messages.values()),'user_id':user_id})
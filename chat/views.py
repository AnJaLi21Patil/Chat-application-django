from django.shortcuts import render, redirect
from .models import Room, Message
from django.contrib.auth.decorators import login_required


# Create your views here.

# @login_required

# def HomeView(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         room = request.POST["room"]
#         try:
#             existing_room = Room.objects.get(room_name__icontains=room)
#         except Room.DoesNotExist:
#             r = Room.objects.create(room_name=room)
#         return redirect("room", room_name=room, username=username)
#     return render(request, "home.html")

@login_required
def HomeView(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip() or "Anonymous"
        room = request.POST.get("room", "").strip()

        Room.objects.get_or_create(
            room_name__iexact=room,
            defaults={"room_name": room}
        )

        return redirect("room", room_name=room, username=username)

    # ✅ USE sender FIELD (NOT username)
    users = (
        Message.objects
        .select_related("room")
        .values("sender", "room__room_name")
        .distinct()
    )

    return render(request, "home.html", {"users": users})


def RoomView(request, room_name, username):
    existing_room = Room.objects.get(room_name__icontains=room_name)
    get_messages = Message.objects.filter(room=existing_room)
    context = {
        "messages": get_messages,
        "user": username,
        "room_name": existing_room.room_name,
    }

    return render(request, "room.html", context)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # use the URL name for HomeView
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework import status

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

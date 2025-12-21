# from django.shortcuts import render, redirect
# from .models import Room, Message
# from django.contrib.auth.decorators import login_required
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from .serializers import RegisterSerializer
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib import messages
# from django.shortcuts import redirect, render
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages



# @login_required
# def HomeView(request):
#     if request.method == "POST":
#         username = request.POST.get("username", "").strip() or "Anonymous"
#         room = request.POST.get("room", "").strip()

#         Room.objects.get_or_create(
#             room_name__iexact=room,
#             defaults={"room_name": room}
#         )

#         return redirect("room", room_name=room, username=username)

#     # ✅ USE sender FIELD (NOT username)
#     users = (
#         Message.objects
#         .select_related("room")
#         .values("sender", "room__room_name")
#         .distinct()
#     )

#     return render(request, "home.html", {"users": users})


# def RoomView(request, room_name, username):
#     existing_room = Room.objects.get(room_name__icontains=room_name)
#     get_messages = Message.objects.filter(room=existing_room)
#     context = {
#         "messages": get_messages,
#         "user": username,
#         "room_name": existing_room.room_name,
#     }

#     return render(request, "room.html", context)


# def login_page(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("home")  # use the URL name for HomeView
#         else:
#             messages.error(request, "Invalid username or password")
#     return render(request, "login.html")



# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# def register_page(request):
#     if request.method == "GET":
#         return render(request, "register.html")

#     if request.method == "POST":
#         response = RegisterView.as_view()(request)

#         # If registration successful
#         if response.status_code == 201:
#             messages.success(request, "Registration successful. Please login.")
#             return redirect("login")

#         # If error, show form again with error
#         messages.error(request, "Registration failed. Try again.")
#         return redirect("register")
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Room, Message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Message



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Room, Message

@login_required
def HomeView(request):
    users = User.objects.exclude(username=request.user.username)
    selected_user = request.GET.get("user")
    messages_list = []
    room_name = None

    if selected_user:
        current_user = request.user.username
        room_name = "_".join(sorted([current_user, selected_user]))
        room, _ = Room.objects.get_or_create(room_name=room_name)
        messages_list = Message.objects.filter(room=room).order_by("timestamp")

    return render(request, "room.html", {
        "users": users,
        "selected_user": selected_user,
        "messages": messages_list,
        "room_name": room_name,
    })

# @login_required
# def RoomView(request, username):
#     current_user = request.user.username
#     other_user = username

#     # Unique room name per user pair
#     room_name = "_".join(sorted([current_user, other_user]))
#     room, _ = Room.objects.get_or_create(room_name=room_name)

#     messages_in_room = Message.objects.filter(room=room).order_by("timestamp")

#     context = {
#         "messages": messages_in_room,
#         "user": current_user,
#         "room_name": room_name,
#         "other_user": other_user
#     }
#     return render(request, "room.html", context)



# @login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Message

# from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Room, Message

# @login_required
# def RoomView(request, username):
#     current_user = request.user.username
#     other_user = username

#     # Unique room name
#     room_name = "_".join(sorted([current_user, other_user]))
#     room, _ = Room.objects.get_or_create(room_name=room_name)

#     # Handle message submission
#     if request.method == "POST":
#         message_text = request.POST.get("message", "").strip()
#         if message_text:
#             Message.objects.create(room=room, sender=current_user, message=message_text)
#         return redirect("room", username=other_user)

#     # Fetch messages
#     messages_in_room = Message.objects.filter(room=room).order_by("timestamp")
#     users = User.objects.exclude(username=current_user)

#     return render(request, "room.html", {
#         "selected_user": other_user,
#         "room_name": room_name,
#         "messages": messages_in_room,
#         "users": users,
#     })
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import Room, Message
# from django.contrib.auth.models import User

@login_required
def RoomView(request, username):
    current_user = request.user.username
    other_user = username

    # Unique room name
    room_name = "_".join(sorted([current_user, other_user]))
    room, _ = Room.objects.get_or_create(room_name=room_name)

    # Fetch messages
    messages_in_room = Message.objects.filter(room=room).order_by("timestamp")
    users = User.objects.exclude(username=current_user)

    return render(request, "room.html", {
        "selected_user": other_user,
        "room_name": room_name,
        "messages": messages_in_room,
        "users": users,
    })

























def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def register_page(request):
    if request.method == "GET":
        return render(request, "register.html")

    if request.method == "POST":
        response = RegisterView.as_view()(request)
        if response.status_code == 201:
            messages.success(request, "Registration successful. Please login.")
            return redirect("login")
        messages.error(request, "Registration failed. Try again.")
        return redirect("register")

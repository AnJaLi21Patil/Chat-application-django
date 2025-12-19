from django.urls import path
from .views import HomeView, login_page, RoomView, register_page

urlpatterns = [
    path('', login_page, name='login'),           # root "/" → login page
    path('home/', HomeView, name='home'),         # HomeView → home.html after login
    path('<str:room_name>/<str:username>/', RoomView, name='room'),
    # path('register/', RegisterView.as_view(), name='register'),  # API register
    path('register/', register_page, name='register'),

]



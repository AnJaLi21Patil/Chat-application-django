from django.urls import path
from .views import HomeView, login_page, RoomView, RegisterView

urlpatterns = [
    path('', login_page, name='login'),           # root "/" → login page
    path('home/', HomeView, name='home'),         # HomeView → home.html after login
    path('<str:room_name>/<str:username>/', RoomView, name='room'),
    path('register/', RegisterView.as_view(), name='register'),  # API register
]
# from django.urls import path
# from .views import login_page, chat_dashboard, RoomView, RegisterView

# urlpatterns = [
#     path('', login_page, name='login'),                     # root "/" → login page
#     path('register/', RegisterView.as_view(), name='register'),  # API or web registration
#     path('dashboard/', chat_dashboard, name='chat-dashboard'),   # home page after login
#     path('room/<str:room_name>/<str:username>/', RoomView, name='room'),
#     path('api/auth/register/', RegisterView.as_view(), name='api-register'), # API
# ]



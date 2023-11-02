#urls для users
from django.urls import path, include
from users import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'users'

urlpatterns = [
path('menu', views.index, name='users_index'),
path('register/', views.register, name='register'),
]
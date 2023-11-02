from django.contrib.auth.models import User
from warehouse_accounting1.models import UserProfile 
from django.shortcuts import render, redirect
from .forms import AdminRegistrationForm


# Після створення користувача в формі реєстрації, отримуємо дані користувача (username і password).
user = User(username='your_username', password='your_password')
user.save()

# Після створення користувача створюємо об'єкт профілю та прив'яжемо його до користувача.
profile = UserProfile(date_of_birth='1990-01-01', profile_picture='profile.jpg', user=user)
profile.save()


users_without_profile = User.objects.filter(userprofile=None)
for user in users_without_profile:
    profile, created = UserProfile.objects.get_or_create(user=user)
 
def some_view(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None

    if user_profile:
        # Робота з user_profile, відобразити профіль користувача
        return render(request, 'profile.html', {'user_profile': user_profile})
    else:
        #якщо відсутній user_profile, перенаправлення на сторінку реєстрації адміністратора
        return redirect('register_admin') 

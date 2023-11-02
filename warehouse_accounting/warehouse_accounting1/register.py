from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegistrationForm  #для створення форми реєстрації

def register(request):
    if request.method == 'POST':
        # Обробка POST-запиту
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Створення користувача з даних форми
            user = form.save()
            
            # Вхід користувача після реєстрації
            login(request, user)
            return redirect('home')
    else:
        # Виведення форми реєстрації 
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from .models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

#обробка сторінки реєстрації користувача
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Авторизуємо користувача
            login(request, new_user)
            user_type = new_user.user_type
            if user_type == User.USERS:
                return redirect('users_index')
            elif user_type == User.WAREHOUSEMAN:
                return redirect('warehouse_accounting1_index')
        else:
            messages.error(request, 'Registration failed. Please check the provided information.')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)

#чи користувач, що робить запит має роль власника
def check_if_owner(request):
    return request.user.user.user_type == User.USERS

def check_if_warehouseman(request):
    return request.user.user.user_type == User.WAREHOUSEMAN

# перевірка типу користувача, що хоче отримати доступ
def index(request):
    user = User.objects.get(name=request.user)
    if str(user.user_type) == "users":
        pass
    elif str(user.user_type) == "warehouseman":
        messages.error(request, 'access denied')
        return redirect('warehouse_accounting1_index')

    return render(request, "warehouse_accounting1/index.html")


# обробка сторінки реєстрації користувачів
def register_page(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            user_type = form.cleaned_data['user_type']
            user_type2 = form.cleaned_data['user_type2']

            User.objects.create(
                user=user,
                name=user.username,
                user_type=user_type,
                user_type2=user_type2,
            )

            messages.success(request, f'Created user {username}')
            return redirect('users_index')
        else:
            print(form.errors)

    context = {
        'form': form,
    }

    return render(request, "users/register.html", context)

#обробка авторизації
def login_page(request):
    if request.user.is_authenticated:
        return render(request, 'warehouse_accounting1/index.html')

    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,
                                username=username,
                                password=password,
                                )

            if user is not None:
                login(request, user)

                if str(User.objects.get(name=username).user_type) == "warehouseman":
                    return redirect('warehouse_accounting1_index')
                elif str(User.objects.get(name=username).user_type) == "users":
                    return redirect('users_index')

    context = {}

    return render(request, "users/login.html", context)

# вихід корстувача з системи
def logout_page(request):
    logout(request)
    return redirect('login')





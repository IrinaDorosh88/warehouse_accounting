from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import authenticate


from users.models import User
#from order.models import Order, OrderItem
from .models import Item, Category
from .forms import NewProductForm, SearchForProduct, NewCategoryForm, SearchForCategory


def index(request):
    # логіка для представлення 'index' 
    return render(request, 'warehouse_accounting1/index.html')


def user_check(request):
    #перевіряти чи user чи warehouseman
    user = User.objects.get(name=request.user)
    return user.user_type == User.WAREHOUSEMAN or user.user_type == User.USERS

#Якщо користувач автентифікований, йому відображається сторінка 'index'. Якщо користувач не автентифікований, 
# він спочатку перенаправляється на сторінку 'login', і після успішної автентифікації його перенаправлять назад на сторінку 'index'.
#@login_required(login_url='login') #перенаправлення на сторінку входу для неавторизованих користувачів
def index(request):
    user = request.user
    return render(request, 'warehouse_accounting1/index.html')

    #розділити список товарів на сторінки і відобразити їх на сторінці з можливістю переходу між сторінками
    products = Item.objects.filter(quantity_on_stock__lt=5)
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    #створити новий продукт (товар) у системі управління складом
#@login_required(login_url='login') #для авторизованих користувачів
#@user_passes_test(user_check, login_url='login')
def create_new_product(request):
    form = NewProductForm()

    if request.method == "POST":
        form = NewProductForm(request.POST)
        if form.is_valid():
            if Item.objects.filter(title=form.cleaned_data['title']).exists():
                messages.error(request, f'"{form.cleaned_data["title"]}" already on stock')
            else:
                new_product = Item.objects.create(
                    title=form.cleaned_data['title'].title(),
                    category=form.cleaned_data['category'],
                    price=form.cleaned_data['price'],
                    description=form.cleaned_data['description'],
                    quantity_on_stock=form.cleaned_data['quantity_on_stock']
                )
                new_product.save()
                messages.success(request, f'"{form.cleaned_data["title"]}" created')
                return redirect('warehouse_accounting1_index')

    context = {
        'form': form,
    }

    return render(request, "warehouse_accounting1/create_new_product.html", context)


#@login_required(login_url='login')
#@user_passes_test(user_check, login_url='login')
def edit_product(request, product_id):
    product = get_object_or_404(Item, id=product_id)

    form = NewProductForm(request.POST or None, instance=product)

    if form.is_valid():
        messages.success(request, f'Product "{product.title}" edited')
        form.save()
        return redirect('display_products')

    context = {
        'form': form,
        'product': product,
    }
    return render(request, "warehouse_accounting1/edit_product.html", context)

#дозволяє редагувати існуючий продукт (товар) у системі управління складом
#@login_required(login_url='login')
#@user_passes_test(user_check, login_url='login')
def display_products(request):
    try:
        products = Item.objects.all()

        paginator = Paginator(products, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj
        }
        return render(request, "warehouse_accounting1/all_products.html", context)

    except ObjectDoesNotExist:
        messages.error(request, "You haven't any product in warehouse")
        return redirect('warehouse_accounting1_index')

#дозволяє відобразити інформацію про конкретний продукт (товар) 
#@login_required(login_url='login')
#@user_passes_test(user_check, login_url='login')
def display_product_info(request, product_id):
    product = get_object_or_404(Item, id=product_id)

    context = {
        'product': product
    }

    return render(request, "warehouse_accounting1/product_info.html", context)

#шукати продукти (товари) на складі за різними параметрами
#@login_required(login_url='login')
#@user_passes_test(user_check, login_url='login')
def search_product(request):
    search_form = SearchForProduct()
    expected_product = []

    if request.method == "POST":
        search_form = SearchForProduct(request.POST)

        if search_form.is_valid():

            # search by title and description
            if search_form.cleaned_data['title'] and search_form.cleaned_data['description']:
                title = search_form.cleaned_data['title']
                description = search_form.cleaned_data['description']
                products = Item.objects.all()

                for product in products:
                    if (title.lower() in str(product).lower()) and (
                            description.lower() in str(product.description).lower()):
                        expected_product.append(product)

            # search by title
            elif search_form.cleaned_data['title']:
                title = search_form.cleaned_data['title']
                products = Item.objects.all()

                for product in products:
                    if title.lower() in str(product).lower():
                        expected_product.append(product)

            # search by description
            elif search_form.cleaned_data['description']:
                description = search_form.cleaned_data['description']
                products = Item.objects.all()

                for product in products:
                    if description.lower() in str(product.description).lower():
                        expected_product.append(product)

            if len(expected_product) == 0:
                messages.error(request, 'Cant find any product')

    context = {
        'search_form': search_form,
        'expected_product': expected_product
    }
    return render(request, 'warehouse_accounting1/search_for_product.html', context)


# дозволяє створювати нову категорію
#@login_required(login_url='login')
#@user_passes_test(user_check, login_url='login')
def create_new_category(request):
    form = NewCategoryForm

    if request.method == "POST":
        form = NewCategoryForm(request.POST)
        if form.is_valid():
            if Category.objects.filter(title=form.cleaned_data['title']).exists():
                messages.error(request, f'Category "{form.cleaned_data["title"]}" already exists')
            else:
                new_category = Category.objects.create(
                    title=form.cleaned_data['title']
                )
                new_category.save()
                messages.success(request, f'Category "{form.cleaned_data["title"]}" created')
                return redirect('/warewarehouse_accounting1')

    context = {
        'form': form
    }

    return render(request, "warehouse_accounting1/add_new_category.html", context)

#дозволяє авторизованим користувачам переглядати всі наявні категорії 
#@login_required(login_url='login')
#@user_passes_test(user_check, login_url='login')
def display_categories(request):
    try:
        categories = Category.objects.all()

        context = {
            'categories': categories
        }

        return render(request, "warehouse_accounting1/all_categories.html", context)

    except ObjectDoesNotExist:
        messages.error(request, "You haven't any categories")
        return redirect('warehouse_accounting1_index')

#дозволяє користувачам шукати категорії
#@login_required(login_url='login')
#@user_passes_test(user_check, login_url='login')
def search_category(request):
    search_form = SearchForCategory()

    if request.method == "POST":
        search_form = SearchForCategory(request.POST)
        if search_form.is_valid():
            title = search_form.cleaned_data['title']
            try:
                category = Category.objects.get(title=title)
                return redirect('category_products', category_id=category.id)
            except ObjectDoesNotExist:
                messages.error(request, 'Cant find category')

    context = {
        'search_form': search_form,
    }

    return render(request, 'warehouse_accounting1/search_for_category.html', context)

#дозволяє користувачам переглядати продукти в певній категорії 
#@login_required(login_url='login')
#@user_passes_test(user_check, login_url='login')
def products_in_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Item.objects.filter(category=category)

    if len(products) > 0:
        context = {
            'products': products
        }
        return render(request, "warehouse_accounting1/category_products.html", context)
    else:
        messages.error(request, f'No products in category "{category}"')
        return redirect('warehouse_accounting1_index')


# дозволяє користувачам змінювати статус закриття замовлення
#@login_required(login_url='login')
#@user_passes_test(user_check, login_url='login')
def change_close_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    order.send_status = False
    order.close_status = True
    order.save()

    messages.success(request, f'Order "{order.order_id}" status: Closed')
    return redirect('warehouse_accounting1_index')


# функця перевірки входу користувача в систему
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
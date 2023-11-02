from django.contrib import admin
from django.urls import path, include
from users import views as users_views
from warehouse_accounting1 import views

urlpatterns = [
    # auth
    path('', views.index, name='index'),
    path('login/', users_views.login_page, name='login'),
    path('logout/', users_views.logout_page, name='logout'),


    path("admin/", admin.site.urls),
    path('users/', include('users.urls')),
    path('warehouse_accounting1', include('warehouse_accounting1.urls')),
]

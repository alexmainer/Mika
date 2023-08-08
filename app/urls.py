
from django.contrib import admin
from django.urls import path
from app import views

app_name = "app"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('libraries/', views.lib, name='libraries'),
    path('contactUs/', views.contact, name='contacts'),
    path('pay', views.pay, name='pay')

]
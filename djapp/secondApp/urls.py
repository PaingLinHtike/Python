from django.contrib import admin
from django.urls import path
from.import views
urlpatterns = [
    path('',views.home,name='home'),
    path('add/',views.add,name='add'),
    path('login/',views.login,name='login'),
    path('index/',views.index,name='index'),
    path('forgot/',views.email_enter,name='email_enter'),
    path('code_enter/',views.code_enter,name='code_enter'),
    path('reset_successful/',views.reset_successful,name='reset_successful'),
    path('successful/',views.successful,name='successful'),

    # Admin
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
]

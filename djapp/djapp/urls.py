from django.contrib import admin #Line 1
from django.urls import path,include #Line 2
urlpatterns = [ #Line 3
    path('',include('secondApp.urls')),
    path('admin/', admin.site.urls),
]

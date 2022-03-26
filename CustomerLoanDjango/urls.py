from django.contrib import admin
from django.urls import path, include
from myapi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('accounts.urls')),
    path('calculator/', include('calc.urls')),
    path('',include('myapi.urls')),
]

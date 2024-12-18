"""R4C URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import orders
import robots
from robots import views
from orders import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_robot/', robots.views.add_robot, name='add_robot'),
    path('generate_excel/', robots.views.generate_excel, name='generate_excel'),
    path('create_order/', orders.views.create_order, name='create_order'),
]

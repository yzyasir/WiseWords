"""wise_words URL Configuration

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
# STEP 3: DONT NEED LINE 17 FOR NOW UNTIL YOU USE ADMIN FEATURE
# from django.contrib import admin

# STEP 2: Have to add include
from django.urls import path, include 

urlpatterns = [
    # path('admin/', admin.site.urls), Dont need to use yet, but when you do uncomment line 17
    
    # STEP 4: Route to out actual urls file in apps folder, if there is none, make it
    path('', include('wise_words_app.urls')) #Here we are telling all the traffic to go to our urls in out app folder, NOT THIS ONE
]

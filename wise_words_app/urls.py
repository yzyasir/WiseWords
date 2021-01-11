# STEP 6: Copy and paste base code form the other urls file
from django.urls import path, include

# STEP 6.5: Tell it that our views file exists, import it
from . import views

urlpatterns = [
    # Here we want to connect our paths with the views file
    path('registerPage', views.registerPage), # STEP 7: If if in views the index method isnt made in views file, make one 
    path('register', views.register), # orange is basically the route we specified, and in views we need to make a method called register 
    path('homepage', views.homepage), # .something is the method we have created in views

    path('loginPage', views.loginPage), # rendering login page here
    path('login', views.login), # method to login

    path('logout', views.logout), # method to logout 

    path('addPost', views.addPost) # link to the add post page
]
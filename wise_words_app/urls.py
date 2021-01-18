# STEP 6: Copy and paste base code form the other urls file
from django.urls import path, include

# STEP 6.5: Tell it that our views file exists, import it
from . import views

urlpatterns = [
    # Here we want to connect our paths with the views file
    path('welcome', views.welcomeToWiseWords),

    path('registerPage', views.registerPage), # STEP 7: If if in views the index method isnt made in views file, make one 
    path('register', views.register), # orange is basically the route we specified, and in views we need to make a method called register 
    path('homepage', views.homepage), # .something is the method we have created in views

    path('loginPage', views.loginPage), # rendering login page here
    path('login', views.login), # method to login

    path('logout', views.logout), # method to logout 

    path('addPost', views.addPost), # link to the add post page
    path('createPost', views.createPost), # route to create a post 

    path('like/<int:postId>', views.likePost), # So do you see how we included the id of the post we are liking? Also, we can name postId variable anything. Doesnt have to be postId.
    path('Unlike/<int:postId>', views.unlikePost),

    path('wiseWords/<int:postId>', views.showPost)
]
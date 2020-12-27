# STEP 6: Copy and paste base code form the other urls file
from django.urls import path, include

# STEP 6.5: Tell it that our views file exists, import it
from . import views

urlpatterns = [
    # Here we want to connect our paths with the views file
    path('', views.index), # STEP 7: If if in views the index method isnt made in views file, make one 
    path('register', views.register) # Orange is basically the route we specified, and in views we need to make a method called register 
]
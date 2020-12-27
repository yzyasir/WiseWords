from django.shortcuts import render, redirect
from django.contrib import messages
# This should help in display the error messages, for one req res cycle

from .models import User # Need to import our models to the views file

# HERE WE RENDER OUR PAGES!!!

# STEP 8: Create your views here. HERE WE MAKE OUR METHODS.
def index(request):
    return render(request, "reg.html") # STEP 9: Need to make an html "templates" file NEXT TO migrations

def register(request): # Things to ask: What am I expecting to return? Render a template? Redirect? Is this method a post req?
    print(request.POST) # This represents information from the POST

    print("*******************")
    
    validationErrorsObject = User.objects.regValidator(request.POST) # This is a function call, so you get something back in the return (errors in our case) 
    # So you need to store what you get back (which I did in validationErrorsObject)
    print(validationErrorsObject)

    print("*******************")

    if len(validationErrorsObject) > 0: # What does .items() do?
        for key, value in validationErrorsObject.items(): # Writing it this way allows me to get the key and value
            messages.error(request, value) # .error is a thing that comes from the messages module that we imported
            # This (request, value) is for all the values in the errors disctionary, WHAT IS REQUEST DOING HERE
        return redirect("/")

    return redirect("/") # post reqs are redirects in python, we redirected to the home page "/""

from django.shortcuts import render, redirect
from django.contrib import messages # This should help in display the error messages, for one req res cycle

import bcrypt # To install, use "pip install bcrypt", this is needed to encypt our passcode

from .models import User # Need to import our models to the views file

# HERE WE RENDER OUR PAGES!!!

# STEP 8: Create your views here. HERE WE MAKE OUR METHODS.
def registerPage(request):
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
    else:

        # Encrypt the passcode, and then create the user
        # hash1 = bcrypt.hashpw('test'.encode(), ) THIS IS AN EXAMPLE
        hashedPasswordVariable = bcrypt.hashpw(request.POST['formPassword'].encode(), bcrypt.gensalt()).decode() # Bcrypt comes in with a method called hashpw
        print(hashedPasswordVariable)

        # See how we dont even have to define newUser, cool no?
        newUser = User.objects.create( # So, you see how we are setting our db fields to whats coming in from the form?
            firstName = request.POST['formFirstName'], 
            lastName = request.POST['formLastName'],
            email = request.POST['formEmail'],
            password = hashedPasswordVariable
            )

        # So to use seesion we want to use the most unique piece of info we can, which is their id
        request.session['loggedInIdForSessions'] = newUser.id  
        # This of request.session as a dictionary of key value pairs that has cookies as values
        # It doesnt let you store the whole user object in session, just primitive data types
        # loggedInIdForSessions is just the key for the object

        # Now that we have made a used cookie for sessions, and created the user, we want to redirect
        return redirect("/homepage")
        # Here we made an object, hence the create
        

    return redirect("/") # post reqs are redirects in python, we redirected to the home page "/""



def homepage(request):
    context = { # Here we are passing in information to the template to display it
        # How do we use information in here, we use the session data since it is stored everywhere
        'loggedInUser' : User.objects.get(id = request.session['loggedInIdForSessions']) # In a dictionary key value pairs are seperated by a colon
    }
    return render(request, "homepage.html", context) #here we are rendering the hompage 
    # Notice how we are passing in context in the return, AFTER ALL A FUNCTION IS ONLY EQUAL TO WHAT IT RETURNS



def loginPage(request):
    return render(request, "login.html") 

def login(request): # redirect becasuse thats what we do in post requests
    # This function will have access being sent from the form so we can print the post data
    print(request.POST) # Once we get this form data, we want to send it through a validator in out models file

    return redirect("/homePage")
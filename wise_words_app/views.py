from django.shortcuts import render, redirect
from django.contrib import messages # This should help in display the error messages, for one req res cycle

import bcrypt # To install, use "pip install bcrypt", this is needed to encypt our passcode

from .models import User # Need to import our models to the views file

# HERE WE RENDER OUR PAGES AND INCLUDE OTHER METHODS !!!

# STEP 8: Create your views here. HERE WE MAKE OUR METHODS.
def registerPage(request):

    # Syntax of a function:
    # def function_name(parameters)
    # whatever you want inside
    # return

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

# _____________________________________________________________________________________________________________________

def homepage(request):
    context = { # Here we are passing in information to the template to display it
        # How do we use information in here, we use the session data since it is stored everywhere
        'loggedInUser' : User.objects.get(id = request.session['loggedInIdForSessions']) # In a dictionary key value pairs are seperated by a colon
    }
    return render(request, "homepage.html", context) #here we are rendering the hompage 
    # Notice how we are passing in context in the return, AFTER ALL A FUNCTION IS ONLY EQUAL TO WHAT IT RETURNS

# ______________________________________________________________________________________________________________________

def loginPage(request): # This is to render
    return render(request, "login.html") 

def login(request): 

    # This will have access being sent from the form so we can print the post data
    print(request.POST) # Once we get this form data, we want to send it through a validator in out models file

    # Why do we put our request.POST inside of this FUNCTION CALL?? Because we want to validate our post data. Basically sending our data to be verified. 
    # Remember what Rahb always said, a function call is only equal to what it returns. So what are we returning? Our errors object.
    validationErrorMessagesObject = User.objects.loginValidator(request.POST) # In this FUNCTION CALL we do User because it is our model, .objects is the structure of data, loginValidator is the validator method in our models file.
    
    if len(validationErrorMessagesObject) > 0: # What does .items() do?
        for key, value in validationErrorMessagesObject.items(): # Writing it this way allows me to get the key and value
            messages.error(request, value) # .error is a thing that comes from the messages module that we imported
            # This (request, value) is for all the values in the errors dictionary, WHAT IS REQUEST DOING HERE

            # print(validationErrorMessagesObject), did this to check in the command line if it worked
        return redirect("/loginPage") # If it doesnt work, then it goes back to the login screen
    
    else:
        userWithAnEmail = User.objects.filter(email = request.POST["formEmail"]) # Else, if we do find the email in request.POST, then make a session using the users id, and then redirect to the home screen
        request.session['loggedInIdForSessions'] = userWithAnEmail[0].id # We use .id (the index of 0) because we want to use the first email we find, since we are not allowing duplicates
        # Note, for the session we are all using the same cookie name "loggedInIdForSessions" for all moments where we use sessions
        return redirect("/homepage") # redirect becasuse thats what we do in post requests
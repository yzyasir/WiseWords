from django.shortcuts import render, redirect
from django.contrib import messages # This should help in display the error messages, for one req res cycle

import bcrypt # To install, use "pip install bcrypt", this is needed to encypt our passcode

from .models import User # Need to import our models to the views file
from .models import Post

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

    
    validationErrorsObject = User.objects.regValidator(request.POST) # This is a function call, so you get something back in the return (errors in our case) 
    # So you need to store what you get back (which I did in validationErrorsObject)
    print(validationErrorsObject)


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
        request.session['loggedInIdForSessions'] = newUser.id  # here we have created sesions
        # This of request.session as a dictionary of key value pairs that has cookies as values
        # It doesnt let you store the whole user object in session, just primitive data types
        # loggedInIdForSessions is just the key for the object

        # Now that we have made a used cookie for sessions, and created the user, we want to redirect
        return redirect("/homepage")
        # Here we made an object, hence the create
        

    return redirect("/") # post reqs are redirects in python, we redirected to the home page "/""

# _____________________________________________________________________________________________________________________

def homepage(request):
    if 'loggedInIdForSessions' not in request.session: # This is basically english LOL! But this checks if you have a cookie created and are in session, if you arent then you'll recieve this error message.
        messages.error(request, "Invalid login Attempt. Please login first.") # The message I have here is basically the value of the message, it can be anything I want
    
        # Note: We didnt use any validations from models, just added one right here, can only do it for one?

        return redirect('/loginPage') # Need to redirect back to the login page, it was giving me an error " 'str' object has no attribute 'get "" when I did not have the redirect

    context = { # Here we are passing in sessions information to the template to display which use has logged in
        # How do we use information in here, we use the session data since it is stored everywhere
        'loggedInUser' : User.objects.get(id = request.session['loggedInIdForSessions']), # In a dictionary key value pairs are seperated by a colon
    # __________________________________________________________________________________________________________________
        # This is to display all of the data for posts using ORM CRUD commands
        'allPosts' : Post.objects.all(), # After typing this out here we go to out html and {{ }} what we named all the posts here...which is allPosts
        # So, before you get fancy using for loops, just try to see what 'allPosts' looks like (hint: it looks like a list)
        
        # This is to display the liked posts
        'likedPosts' : Post.objects.filter(likes=User.objects.get(id = request.session['loggedInIdForSessions'])), # HERE I AM A BIT CONFUSED
        # This is to not display the ones we've liked on the table (HERE WE USED THE EXCLUDE ORM COMMAND)
        'notLikedPosts' : Post.objects.exclude(likes=User.objects.get(id = request.session['loggedInIdForSessions'])) # HERE I AM A BIT CONFUSED
    # __________________________________________________________________________________________________________________
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

# __________________________________________________________________________________________________________________________

def logout(request):

    # Not only do we want to be redirected when we logout, we want to clear the cookie, otherwise the user will stay logged in
    request.session.clear() # Use this to clear the session cookie

    # Note: We are not using any validations right? So we dont need to do anything in the models file
    return redirect("/loginPage")

# __________________________________________________________________________________________________________________________

def addPost(request):
    return render(request, "addPost.html") # We are not passing anything like sessions here (if you look at the homepage and register function above)

def createPost(request): # the name of the route is the same as the method name 

    newPost = Post.objects.create(
        wiseWords = request.POST['formPost'], 
        uploader = User.objects.get(id = request.session['loggedInIdForSessions'])) 
            # See how we are setting the data from the form using request.POST and setting it equal to the database term
            # Pulled from line 74 and set it to 128, basically getting the id from sessions and then setting it to id
            # What is did in line 127 is that I got the data from sessions, set it to id, and then set that to uploader

    return redirect("/homepage")

# __________________________________________________________________________________________________________________________
def likePost(request, postId): # Notice: We need to enter the variable for the id of the post we are likeing into the parameters
# print(postId) # Before doing anything, just check if id even shows in the console

    # Here we will be making the many to many join
    userThatIsLikingThePost = User.objects.get(id = request.session['loggedInIdForSessions']) # Again, this is how we use sessions and get the user who is logged in
    rantThatIsBeingLiked = Post.objects.get(id=postId) # TRY AND UNDERSTAND THIS PART A BIT MORE 
    # I BELIEVE WE GOT THE TWO OBJECTS THAT WE WANT TO MAKE THE JOIN FOR AS VARIABLES
    
    # NOW WE CAN USE EITHER ONE TO MAKE THE RELATIONSHIP
    userThatIsLikingThePost.posts_liked.add(rantThatIsBeingLiked) # posts_liked is the related name from the models, same as post_uploader (also from the models file)
    # Or you can do: rantThatIsBeingLiked.post_uploader.add(userThatIsLikingThePost)
    # The only reason why we are able to do this is because in posts model their is already a many to many relationship made

    # Then redirect
    return redirect("/homepage")


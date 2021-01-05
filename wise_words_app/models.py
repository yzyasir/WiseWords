from django.db import models

import re #allows us to import regex

# Create your models AND validations here. 

# 2nd Step Models: Here we are doing validations for register
# We will pass request.POST (here it will be refered to as postDataFromTheForm) to this function
class UserManager(models.Manager): # Did TableNameManager,    this manager is used to validate anything regarding users, so we can have multiple methods inside of one class
    
    def loginValidator(self, postDataFromTheLoginForm):
        errors = {} 

        return errors 
    
    def regValidator(self, postDataFromTheForm): # Can name that anything I want so I made it long
        errors = {} # Here we will have our errors in a "dictionary", each key name must be unique

        # All regex means is regular expression/patterns (of emails in our case)
        # The blue r indicates a raw string, shows that any of the symbols are allowed, hten the at symbol, then what is shown after the at is allowed, then it needs a .
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # .compile turns a regular expression string into an object, that we can compare strings with

        # Here we we'll have validation if checks
        if len(postDataFromTheForm['formFirstName']) == 0:
            errors['firstNameReq'] = "First Name Is Required" 

        if len(postDataFromTheForm['formLastName']) == 0:
            errors['lastNameReq'] = "Last Name Is Required"

        if len(postDataFromTheForm['formEmail']) == 0:
            errors['emailReq'] = "Email Is Required"

        if len(postDataFromTheForm['formPassword']) < 4:
            errors['passwordReq'] = "Password Must Be At Least 4 Characters Long"

        if postDataFromTheForm['formPassword'] != postDataFromTheForm['formConfirmPW']: # != means not equal
            errors['confirmPWReq'] = "The Passwords Must Match, Please Try Again"
        
        # The below code means if they do not match the pattern, what the blue not is for.
        elif not EMAIL_REGEX.match(postDataFromTheForm['formEmail']):  # test whether a field matches the pattern            
            errors['errors_email'] = "Email Must Be In Proper Format!"
        else:
            email_taken = User.objects.filter(email = postDataFromTheForm['formEmail']) # What .filter does is that it filters the database for the email that comes through the form
            # If the length of this email is greater than 0, then the email is taken, note formEmail is put into a list/list
            if len(email_taken)>0: 
                errors['errors_email_taken'] = "This Email Is Taken. Please Try Again." # This errors message is going into the errors dictionary
        # Whole else statement PREVENTS DUPLICATE EMAILS
        
        return errors

 
# Note: Creating a db requires migration commands, but we have nothing to migrate...
# So lets give it some instructions for db tables

# 1st Step Models: Its gonna be our db table, so we need to inherit from models
class User(models.Model):
    # id is made by itself and theres no need to make it yourself, here but its hidden if you like to think that way

    firstName = models.CharField(max_length=15)
    lastName = models.CharField(max_length=15)
    email = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager() #must connect the validatons to our user models
    # Objects needs to be in the right location (I typically add this portion after migrations)
    # objects = models.Manager(), This, like id, is is naturally assumed to be here (but its hidden)
    # models.Manager() allows us to have different features like .create, .update, .all, .delete, etc

    # IMPORTANT: Once this is all typed in do your migrations, after killing the server
    # To create the models you put in, you must enter this this commands into the terminal:
    # "python manage.py runserver" 

    # To apply all migrations, enter this into the terminal:
    # "python manage.py migrate"

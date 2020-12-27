from django.db import models

# Create your models AND validations here. 

# 2nd Step Models: Here we are doing validations for register
# We will pass request.POST (here it will be refered to as postDataFromTheForm) to this function
class UserManager(models.Manager): # Did TableNameManager
    def regValidator(self, postDataFromTheForm): # Can name that anything I want so I made it long
        errors = {} # Here we will have our errors in a "dictionary", each key name must be unique

        # Here we we'll have validation if checks
        if len(postDataFromTheForm['firstName']) == 0:
            errors['firstNameReq'] = "First Name Is Required" 

        if len(postDataFromTheForm['lastName']) == 0:
            errors['lastNameReq'] = "Last Name Is Required"

        if len(postDataFromTheForm['email']) == 0:
            errors['emailReq'] = "Email Is Required"

        if len(postDataFromTheForm['password']) < 4:
            errors['passwordReq'] = "Password Must Be At Least 4 Characters Long"

        if postDataFromTheForm['password'] != postDataFromTheForm['confirmPW']: # != means not equal
            errors['confirmPWReq'] = "The passwords must match, please try again"
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

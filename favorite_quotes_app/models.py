from django.db import models
import bcrypt, re

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if User.objects.filter(email=postData['email']):
            errors['duplicate_email'] = "There is already a user registered with that email address"
        if len(postData['f_name']) < 2:
            errors['f_name_length'] = "Please provide a valid first name (two characters or more)"
        if len(postData['l_name']) < 2:
            errors['l_name_length'] = "Please provide a valid last name (two characters or more)"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = "Invalid email address!"
        if postData['pw_conf'] != postData['pw']:
            errors['pw_conf_match'] = "Confirmation password and password must match!" 
        return errors
    def update_validator(self, postData):
        errors = {}
        if len(postData['f_name']) < 2:
            errors['f_name_length'] = "Please provide a valid first name (two characters or more)"
        if len(postData['l_name']) < 2:
            errors['l_name_length'] = "Please provide a valid last name (two characters or more)"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = "Invalid email address!"
        return errors
    def login_validator(self, postData):
        errors = {}
        user_test = User.objects.filter(email = postData['email2'])
        if user_test:
            if not bcrypt.checkpw(postData['pw2'].encode(), user_test[0].pw.encode()): 
                errors['bad_pw'] = "Bad email-password combination"
        else:
            errors['no_such_user'] = "Bad email-password combination"
        return errors
    def quote_validator(self, postData):
        errors = {}
        if len(postData['quote_txt']) < 11:
            errors['min_quote_length'] = "Please submit a longer quote (more than 10 characters)!"
        if len(postData['attr_author']) < 4:
            errors['author_name_length'] = "Please provide a valid author name (more than 3 characters)!"
        return errors

class User(models.Model):
    f_name = models.CharField(max_length=40)
    l_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    pw = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    quote_txt = models.TextField()
    attr_author = models.CharField(max_length=40, null=True)
    uploaded_by = models.ForeignKey(User, related_name="uploaded_quotes", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
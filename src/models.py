from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
# Create your models here.


class subcription(models.Model):
    plan_choice = (
        ('Basic','Basic'),
        ('Advance','Advance'),
        ('Premium','Premium'),
    )
    plan_name = models.CharField(max_length=100)
    post_limit = models.IntegerField(default=0)
    plan_type = models.CharField(max_length=50 , choices=plan_choice)

    def __str__(self):
        return self.plan_name  +""+ self.plan_type

class user_profile(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription    = models.ForeignKey(subcription, on_delete=models.CASCADE , related_name="mysubs" , null=True , blank=True)
    name            = models.CharField(max_length=100)
    phone           = models.CharField(max_length=25)
    email           = models.EmailField(max_length=100)
    image           = models.FileField(upload_to="Profile" , default="default.png")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name  +""+ self.phone
   
    
class blog_category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class blog(models.Model):
    user = models.ForeignKey(user_profile, on_delete=models.CASCADE , related_name='my_blogs')
    title = models.CharField(max_length=100)
    description = HTMLField()
    category = models.ForeignKey(blog_category ,on_delete=models.CASCADE , related_name='blog_cat' )
    is_verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def pub_date_pretty(self):
        return self.date.strftime('%b %e %Y')
    







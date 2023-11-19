from django import forms
from .models import *
from tinymce.widgets import TinyMCE
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) < 10 or len(phone) > 25:
            raise ValidationError("Phone number must be between 10 and 25 characters.")
        return phone
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3 :
            raise ValidationError("please enter more than 3 words for username")
        return name

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'phone', 'password1', 'password2']



# forms.py


class UserProfileForm(forms.ModelForm):
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) < 10 or len(phone) > 25:
            raise ValidationError("Phone number must be between 10 and 25 characters.")
        return phone
    
    
    class Meta:
        model = user_profile
        fields = ['name', 'phone', 'email', 'image']


class AddBlog(forms.ModelForm):
    # date = forms.DateField(label="Date",required=True, widget=NumberInput(attrs={'type':'date' , "class": "form-control"}))
    class Meta:
        model = blog
        exclude = ('user','is_verified',)

        widgets = {
                'title': forms.TextInput(attrs={'class': 'form-control mb-5'}),
                'description': TinyMCE(attrs={'cols': 80, 'rows': 30 , 'class':'mb-5'}) ,
                'category': forms.Select(attrs={'class': 'form-control'})
                   
                   }





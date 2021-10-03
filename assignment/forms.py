from django.db.models import fields
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm

class User_Form(forms.ModelForm):
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name','last_name','email']
class Teacher_User_Form(forms.ModelForm):
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = Teacher_User
        fields = ['post',]
# class HOD_Form(forms.ModelForm):
#     class Meta:
#         model = HOD_User
#         fields = ['department']


class UserCreationForm(forms.ModelForm):
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name','last_name','email',]
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')

    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError('Passwords don\'t match')
    #     return password2

    # def save(self, commit=True):
    #     user = super(CustomCreationForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data['password2'])
    #     if commit:
    #         user.save()
    #     return user


class CustomCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name','last_name','email']
    

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super(CustomCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


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


class Batch_Create_Form(forms.ModelForm):
    """Form definition for Batch_Create_."""
    class Meta:
        """Meta definition for Batch_Create_form."""
        model = Batch
        fields = ('name','semester',)


class Semester_Create_Form(forms.ModelForm):
    """Form definition for Batch_Create_."""
    class Meta:
        """Meta definition for Batch_Create_form."""
        model = Semester
        fields = ('name',)

    # def __init__(self, *args, **kwargs):

    #     self.request = kwargs.pop('request')
    #     super(Semester_Create_Form, self).__init__(*args, **kwargs)
    #     self.fields['courses'].queryset = Course.objects.filter(
    #         department=self.request.user.hod.department)
    name = forms.CharField()
    # courses = forms.ModelMultipleChoiceField(
    #     queryset=Course.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    
    

class Student_Create_Form(forms.ModelForm):
    """Form definition for Student_Create_."""

    class Meta:
        """Meta definition for Student_Create_form."""

        model = Student_User
        fields = ('reg_no','roll_no',)
    
    
    def __init__(self, *args, **kwargs):
        super(Student_Create_Form, self).__init__(*args, **kwargs)
        self.fields['roll_no'].widget.attrs['required'] = 'required'


# class Subject_Create_Form(forms.ModelForm):
#     """Form definition for Subject_."""
#     class Meta:
#         """Meta definition foCreate_r Subject_form."""
#         model= Subject
#         fields = ('subject_code', 'name',)


class Course_Create_Form(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('subject_name', 'subject_code', 'teacher','semester')
    
    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request')
        super(Course_Create_Form, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = Teacher_User.objects.filter(
            department=self.request.user.hod.department)
        self.fields['semester'].queryset = Semester.objects.filter(
            department=self.request.user.hod.department)
    # courses = forms.ModelMultipleChoiceField(
    #     queryset=Course.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )


class Assignment_Form(forms.ModelForm):
    """Form definition for Assignment."""

    class Meta:
        """Meta definition for Assignmentform."""

        model = Assignment
        fields = ('title','description','file',)

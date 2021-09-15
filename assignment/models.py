from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class Department(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class User(AbstractUser):
    OPTIONS=(
        ('HOD','HOD'),
        ('Teacher','Teacher'),
        ('Clerk','Clerk'),
        ('Student','Student'),
    )
    username = None

    role = models.CharField(choices=OPTIONS,max_length=12, error_messages={
        'required': "Role must be provided"
    })

    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    department = models.ForeignKey(Department,related_name='Users',null=True,blank=True,on_delete=models.CASCADE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','last_name']

    def __unicode__(self):
        return self.email

    objects = UserManager()

class StudentUser(User):
    reg_no = models.CharField(max_length=255)
    roll_no = models.IntegerField()

    class Meta:
        verbose_name = 'Student_User'
    


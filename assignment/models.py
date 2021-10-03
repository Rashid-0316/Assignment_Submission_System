from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db.models.signals import post_save


# class University(models.Model):
#     name = models.CharField(max_length=250)

#     def __str__(self):
#         return self.name

class Department(models.Model):
    name = models.CharField(max_length=250)
    hod=models.OneToOneField("HOD_User",related_name='department',null=True,blank=True,on_delete=models.SET_NULL)
    # university=models.ForeignKey(University,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class User(AbstractUser):
    OPTIONS=(
        ('hod','hod'),
        ('teacher','teacher'),
        ('clerk','clerk'),
        ('student','student'),
    )
    username = None
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    # university=models.ForeignKey(University,null=True,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile_pictures')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','last_name']
    user_type= models.CharField(choices=OPTIONS,max_length=20)
    is_hod=models.BooleanField(default=False)
    is_teacher=models.BooleanField(default=False)
    is_clerk=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)

    def __unicode__(self):
        return self.email

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.user_type=='hod':
            self.is_hod=True
        elif self.user_type=='teacher':
            self.is_teacher=True
        elif self.user_type=='clerk':
            self.is_clerk=True
        elif self.user_type=='student':
            self.is_student=True
        super().save(*args, **kwargs)  # Call the "real" save() method.

class HOD_User(models.Model):
    hod=models.OneToOneField(User,null=True,blank=True,related_name='hod',on_delete=models.CASCADE)
    # department = models.OneToOneField(Department,related_name='hodUser',blank=True,null=True,on_delete=models.SET_NULL)
    date_created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.hod)
    class Meta:
        verbose_name = ("HOD")
        verbose_name_plural = ("HODS")



class Clerk_User(models.Model):
    clerk=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,blank=True,null=True,on_delete=models.CASCADE)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.clerk)
    
    class Meta:
        verbose_name = ("Clerk")
        verbose_name_plural = ("Clerks")

class Teacher_User(models.Model):
    OPTIONS=(
        ('Professor','Professor'),
        ('Assistent Professor','Assistent Professor'),
        ('Lecturer','Lecturer'),
        ('Visiting Lecturer','Visiting Lecturer'),
    )
    teacher=models.OneToOneField(User,related_name='teacher_user',null=True,blank=True,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,blank=True,null=True,on_delete=models.CASCADE)
    post=models.CharField(choices=OPTIONS,max_length=250)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.teacher)
    class Meta:
        verbose_name = ("Teacher")
        verbose_name_plural = ("Teachers")



class Student_User(models.Model):
    student=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,blank=True,null=True,on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=255)
    roll_no = models.IntegerField()
    date_created=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Student_User'
    
    def __str__(self):
        return str(self.student)
    
    class Meta:
        verbose_name = ("Student")
        verbose_name_plural = ("Students")
    
def create_profile(sender, instance,created,**kwargs):
    if created:
        if instance.user_type=='hod':
            HOD_User.objects.create(hod=instance)
        elif instance.user_type=='clerk':
            Clerk_User.objects.create(clerk=instance)
        elif instance.user_type=='student':
            Student_User.objects.create(student=instance)

post_save.connect(create_profile, sender=User)
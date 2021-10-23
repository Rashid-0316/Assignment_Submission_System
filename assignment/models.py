from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from .manager import UserManager
from django.db.models.signals import post_save
from django.utils.timezone import now
from django.urls import reverse

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


# class Subject(models.Model):
#     """Model definition for Subject."""
#     subject_code=models.CharField(max_length=250)
#     name = models.CharField(max_length=250)
#     department = models.ForeignKey(
#         Department, related_name='subject', null=True, blank=True, on_delete=models.CASCADE)


#     class Meta:
#         """Meta definition for Subject."""

#         verbose_name = 'Subject'
#         verbose_name_plural = 'Subjects'

#     def __str__(self):
#         """Unicode representation of Subject."""
#         return self.name

class Semester(models.Model):
    """Model definition for Semester."""
    name = models.CharField(max_length=250)
    # courses=models.ManyToManyField("Course",null=True,blank=True,related_name='semester_course')
    department = models.ForeignKey(Department,related_name='semesters',null=True, blank=True, on_delete=models.CASCADE)
    class Meta:
        """Meta definition for Semester."""
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'

    def __str__(self):
        """Unicode representation of Semester."""
        return self.name

    
class Course(models.Model):
    """Model definition for Course."""

    subject_name = models.CharField(max_length=250, null=True, blank=True)
    subject_code = models.CharField(max_length=250,null=True,blank=True)
    teacher=models.ForeignKey(Teacher_User,related_name='courses_of_teacher',on_delete=models.CASCADE,null=True,blank=True)
    semester = models.ForeignKey(Semester, related_name='courses',
                                on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(
        Department, related_name='course', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Course."""

        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.subject_name


def assignement_create_path(instance, filename):
    # path = f"assignments/{instance.subject.department.id}/{instance.subject.department}/{instance.subject.semester}/{instance.subject}/"
    return 'assignments/{0}/{1}/{2}/{3}'.format(instance.subject.department.id, instance.subject.semester, instance.subject, filename)
class Assignment(models.Model):
    subject = models.ForeignKey(Course, related_name='assignments',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description=models.TextField(null=True,blank=True)
    file = models.FileField(upload_to=assignement_create_path, max_length=100)

    def __str__(self):
        return self.title


def assignement_submit_path(instance, filename):
    # path = f"assignments/{instance.subject.department.id}/{instance.subject.department}/{instance.subject.semester}/{instance.subject}/"
    return 'submission/{0}/{1}/{2}/{3} {4}/{5}'.format(instance.student.department.id, instance.student.batch.semester, instance.assignment, instance.student.roll_no, instance.student.student.first_name, filename)
class Assignment_Submission(models.Model):
    student = models.ForeignKey("Student_User", related_name='assign_of_student', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='solutions', on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    file = models.FileField(upload_to=assignement_submit_path, max_length=100)
    
    class Meta:
        """Meta definition for Assignment_Submission."""

        verbose_name = 'Assignment_Submission'
        verbose_name_plural = 'Assignment_Submissions'

    def __str__(self):
        return f"Roll no {self.student.roll_no} {self.student.department} {self.student.batch}"

class Batch(models.Model):
    name = models.CharField(max_length=250)
    semester=models.ForeignKey(Semester,null=True,blank=True,on_delete=models.CASCADE)
    department=models.ForeignKey(Department,null=True,blank=True,on_delete=models.CASCADE)
    class Meta:
        verbose_name = ("batch")
        verbose_name_plural = ("batches")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("batch_detail", kwargs={"pk": self.pk})


class Student_User(models.Model):
    student=models.OneToOneField(User,related_name='student_user',null=True,blank=True,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,blank=True,null=True,on_delete=models.CASCADE)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE,related_name='students',null=True,blank=True)
    reg_no = models.CharField(max_length=255)
    roll_no = models.IntegerField(null=True,blank=True)
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

post_save.connect(create_profile, sender=User)

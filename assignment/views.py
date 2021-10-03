
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import *
from .forms import *
# from .models import *
from django.urls import reverse
from .decorators import SuperRequiredMixin
from .models import User
from django.core.mail import send_mail


# Create your views here.

class LandingPage(TemplateView):
    template_name = "landing_page.html"


class DepttListView(SuperRequiredMixin,ListView):
    model = Department
    context_object_name='departments'
    template_name = "admin/deptt-listview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["departments_count"] = Department.objects.all().count()
        context["hod_count"] = HOD_User.objects.all().count()
        context["teachers_count"] = Teacher_User.objects.all().count()
        context["students_count"] = Clerk_User.objects.all().count()
        context["clerks_count"] = Student_User.objects.all().count()

        return context

class DepttDetailView(SuperRequiredMixin,DetailView):
    model = Department
    context_object_name='department'
    template_name = "admin/deptt-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department=self.get_object()
        if department.hod:
            hod_id=department.hod.id
            hod_user=get_object_or_404(HOD_User,id=hod_id)
            context["user_id"]=hod_user.hod.id
            context["user_object"]=get_object_or_404(User,id=hod_user.hod.id)
            context["hod_id"] = hod_id

        return context

class DepttCreateView(SuperRequiredMixin,CreateView):
    model = Department
    fields = "__all__"
    template_name = "admin/department.html"

    def get_success_url(self):
        return reverse('deptt-list-view')

class DepttUpdateView(SuperRequiredMixin,UpdateView):
    model = Department
    fields = "__all__"
    template_name = "admin/DepttUpdate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dept=self.get_object()
        print(dept)
        print(dept.hod)
        if dept.hod !=None:
            hod_id= dept.hod.id
            hod_user=HOD_User.objects.filter(id=hod_id)[0]
            user_id=hod_user.hod.id
            context["hod_id"] =hod_id
            context["user_id"]=user_id
        context['name']=dept.name
        context['id']=dept.id
        return context
    
    
    def get_success_url(self):
        return reverse('deptt-list-view')



class DepttDeleteView(SuperRequiredMixin,DeleteView):
    model = Department
    template_name = "admin/deptt-delete.html"



class HODCreateView(SuperRequiredMixin,CreateView):
    form_class = User_Form
    template_name = "registration/signup.html"


    def get_success_url(self):
        return reverse('deptt-list-view')


    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        hod = form.save(commit=False)
        password = User.objects.make_random_password(length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889") # zvk0hawf8m6394
        hod.set_password(password)
        hod.user_type='hod'
        hod_email=hod.email
        hod.role = 'HOD'
        hod.save()
        send_mail(
            subject='Account Created',
            message='your account has been created with your email and password is '+password,
            from_email="test@gmail.com",
            recipient_list=[hod_email,],
            fail_silently=False,
            
        )
        
        return super().form_valid(form)


class HODUpdateView(SuperRequiredMixin,UpdateView):
    model = User
    deptt_id=0
    fields = ['first_name','last_name','email']
    template_name = "admin/hod-update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        user = get_object_or_404(User,id=id)
        hod_id=user.hod.id
        hod_user=get_object_or_404(HOD_User,id=hod_id)
        HODUpdateView.deptt_id=hod_user.department.id
        context["hod_id"] =user.id
        context["deptt_id"]=HODUpdateView.deptt_id
        return context
    
    
    def get_success_url(self):
        return reverse('deptt-detail-view',kwargs={'pk':HODUpdateView.deptt_id})


class HODListView(SuperRequiredMixin,ListView):
    queryset=User.objects.filter(user_type='hod')
    context_object_name='hods'
    template_name = "admin/hod-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # hod=self.hod.hod
        # context["department"] = hod.department
        return context
    


class HODDeleteView(SuperRequiredMixin,DeleteView):
    model = User
    template_name = "admin/hod-delete.html"

    def get_success_url(self):
        return reverse('deptt-list-view')

# HOD views start from here


# class HOD_Dashboard_ListView(ListView):
    
#     queryset=get_object_or_404(Teacher_User,)
#     context_object_name='current_department'
#     template_name = "HOD/hod-dashboard.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         request=self.request
#         department=request.department
#         context["clerks"] = User.objects.filter(role='Clerk',department=department)
#         context["teachers_count"] = User.objects.filter(role='Teacher',department=department).count()
#         context["students_count"] = User.objects.filter(role='Student',department=department).count()
#         context["clerks_count"] = User.objects.filter(role='Clerk',department=department).count()
#         return context

def HOD_Dashboard(request):
    user=request.user.hod
    teachers=Teacher_User.objects.filter(department=user.department)
    students=Student_User.objects.filter(department=user.department)
    # teacher_user=User.objects.filter(is_teacher=True)
    # teachers=User.teacher_user.filter(department=user.department)

    context={
        'user':user,
        'teachers':teachers,
        'students':students,
    }
    
    return render(request,'HOD/hod-dashboard.html',context)

def Teacher_list_View(request):
    user=request.user.hod
    teachers=Teacher_User.objects.filter(department=user.department)

    context={
        'user':user,
        'teachers':teachers,
    }
    
    return render(request,'HOD/teacher_list.html',context)



def Teacher_Create_View(request):

    if request.method == 'POST':
        form1 = User_Form(request.POST)
        form2=Teacher_User_Form(request.POST)
        if form1.is_valid() and form2.is_valid():
            email=form1.cleaned_data['email']
            user = form1.save(commit=False)
            user.user_type='teacher'
            password = User.objects.make_random_password(length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889") # zvk0hawf8m6394
            user.set_password(password)
            
            send_mail(
                subject='Account Created',
                message='your account has been created with your email and password is '+password,
                from_email="test@gmail.com",
                recipient_list=[email,],
                fail_silently=False,
                
            )
            user.save()
            teacher = form2.save(commit=False)
            teacher.teacher=user
            hod=request.user.hod.department
            teacher.department=hod
            teacher.save()
            return redirect('hod-dashboard')

    else:
        form1 = User_Form(request.POST)
        form2=Teacher_User_Form(request.POST)
    
    return render(request,'HOD/teacher-create-view.html',{'form1':form1,'form2':form2})


def Teacher_Update_View(request,pk):
    user=get_object_or_404(User,id=pk)
    teacher=user.teacher_user
    if request.method == 'POST':
        form1 = User_Form(request.POST or None,instance=user)
        form2=Teacher_User_Form(request.POST or None,instance=teacher)
        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            user.user_type='teacher'
            user.save()
            teacher = form2.save(commit=False)
            teacher.teacher=user
            hod=request.user.hod.department
            teacher.department=hod
            teacher.save()
            return redirect('hod-dashboard')

    else:
        form1 = User_Form(request.POST or None,instance=user)
        form2=Teacher_User_Form(request.POST or None,instance=teacher)
    
    return render(request,'HOD/teacher-create-view.html',{'form1':form1,'form2':form2})


def Teacher_delete_View(request,pk):
    user=get_object_or_404(User,id=pk)
    user.delete()
    return redirect('hod-dashboard')

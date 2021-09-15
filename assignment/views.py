
from django.shortcuts import get_object_or_404, render
from django.views.generic import *
from .forms import *
from .models import *
from django.urls import reverse
from .decorators import SuperRequiredMixin
from .models import User
from django.core.mail import send_mail


# Create your views here.

class LandingPage(TemplateView):
    template_name = "landing_page.html"


class DepttListView(SuperRequiredMixin,ListView):
    model = User
    queryset=User.objects.filter(role='HOD')
    context_object_name='hods'
    template_name = "listview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teachers_count"] = User.objects.filter(role='Teacher').count()
        context["students_count"] = User.objects.filter(role='Student').count()
        context["clerks_count"] = User.objects.filter(role='Clerk').count()
        context["hods_count"] = User.objects.filter(role='HOD').count()

        return context

class DepttDetailView(SuperRequiredMixin,DetailView):
    model = User
    context_object_name='hod'
    template_name = "DepttDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hod=self.get_object()
        deptt=hod.department
        context["id"] = deptt.id
        return context

class DepttCreateView(SuperRequiredMixin,CreateView):
    model = Department
    fields = "__all__"
    template_name = "department.html"

    def get_success_url(self):
        return reverse('')

class DepttUpdateView(SuperRequiredMixin,UpdateView):
    model = Department
    fields = "__all__"
    template_name = "DepttUpdate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        dept=Department.objects.filter(id=id)
        hod= dept[0].Users.filter(role='HOD')
        context["hod"] =hod[0].id
        context["id"]=id
        context['name']=dept[0]
        return context
    
    
    def get_success_url(self):
        return reverse('')




class HODCreateView(SuperRequiredMixin,CreateView):
    form_class = HODCreationForm
    template_name = "registration/signup.html"


    def get_success_url(self):
        return reverse('deptt-list-view')


    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        hod = form.save(commit=False)
        password = User.objects.make_random_password(length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889") # zvk0hawf8m6394
        hod.set_password(password)
        
        
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
    fields = ['first_name','last_name','email']
    template_name = "hod-update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        hod = get_object_or_404(User,id=id)
        deptt=hod.department
        deptt_id=deptt.id
        context["hod_id"] =hod.id
        context["deptt_id"]=deptt_id
        context["deptt_name"] = deptt.name
        return context
    
    
    def get_success_url(self):
        return reverse('/')


class HODListView(SuperRequiredMixin,ListView):
    queryset=User.objects.filter(role='HOD')
    context_object_name='hods'
    template_name = "hod-list.html"


class HODDeleteView(SuperRequiredMixin,DeleteView):
    model = User
    template_name = "hod-delete.html"

    def get_success_url(self):
        return reverse('hod-list-view')



# HOD views start from here


class HOD_Dashboard_ListView(ListView):
    queryset=User.objects.filter(role='Teacher')
    context_object_name='current_department'
    template_name = "HOD/hod-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request=self.request
        department=request.department
        context["clerks"] = User.objects.filter(role='Clerk',department=department)
        context["teachers_count"] = User.objects.filter(role='Teacher',department=department).count()
        context["students_count"] = User.objects.filter(role='Student',department=department).count()
        context["clerks_count"] = User.objects.filter(role='Clerk',department=department).count()
        return context

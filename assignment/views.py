
from django.core.checks import messages
from django.db.models.aggregates import StdDev
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import *
from .forms import *
# from .models import *
from django.urls import reverse
from .decorators import *
from .models import User
from django.core.mail import send_mail
from django.contrib import messages


# Create your views here.
def error_404(request, exception):
    return render(request, '404.html',)


class LandingPage(TemplateView):
    template_name = "landing_page.html"


class DepttListView(SuperRequiredMixin, ListView):
    model = Department
    context_object_name = 'departments'
    template_name = "admin/deptt-listview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["departments_count"] = Department.objects.all().count()
        context["hod_count"] = HOD_User.objects.all().count()
        context["teachers_count"] = Teacher_User.objects.all().count()
        context["students_count"] = Clerk_User.objects.all().count()
        context["clerks_count"] = Student_User.objects.all().count()

        return context


class DepttDetailView(SuperRequiredMixin, DetailView):
    model = Department
    context_object_name = 'department'
    template_name = "admin/deptt-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        if department.hod:
            hod_id = department.hod.id
            hod_user = get_object_or_404(HOD_User, id=hod_id)
            context["user_id"] = hod_user.hod.id
            context["user_object"] = get_object_or_404(
                User, id=hod_user.hod.id)
            context["hod_id"] = hod_id

        return context


class DepttCreateView(SuperRequiredMixin, CreateView):
    model = Department
    fields = "__all__"
    template_name = "admin/department.html"

    def get_success_url(self):
        return reverse('deptt-list-view')


class DepttUpdateView(SuperRequiredMixin, UpdateView):
    model = Department
    fields = "__all__"
    template_name = "admin/DepttUpdate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dept = self.get_object()
        print(dept)
        print(dept.hod)
        if dept.hod != None:
            hod_id = dept.hod.id
            hod_user = HOD_User.objects.filter(id=hod_id)[0]
            user_id = hod_user.hod.id
            context["hod_id"] = hod_id
            context["user_id"] = user_id
        context['name'] = dept.name
        context['id'] = dept.id
        return context

    def get_success_url(self):
        return reverse('deptt-list-view')


class DepttDeleteView(SuperRequiredMixin, DeleteView):
    model = Department
    template_name = "admin/deptt-delete.html"


class HODCreateView(SuperRequiredMixin, CreateView):
    form_class = User_Form
    template_name = "registration/signup.html"

    def get_success_url(self):
        return reverse('deptt-list-view')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        hod = form.save(commit=False)
        password = User.objects.make_random_password(
            length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")  # zvk0hawf8m6394
        hod.set_password(password)
        hod.user_type = 'hod'
        hod_email = hod.email
        hod.role = 'HOD'
        hod.save()
        send_mail(
            subject='Account Created',
            message='your account has been created with your email and password is '+password,
            from_email="test@gmail.com",
            recipient_list=[hod_email, ],
            fail_silently=False,

        )

        return super().form_valid(form)


class HODUpdateView(SuperRequiredMixin, UpdateView):
    model = User
    deptt_id = 0
    fields = ['first_name', 'last_name', 'email']
    template_name = "admin/hod-update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        user = get_object_or_404(User, id=id)
        hod_id = user.hod.id
        hod_user = get_object_or_404(HOD_User, id=hod_id)
        HODUpdateView.deptt_id = hod_user.department.id
        context["hod_id"] = user.id
        context["deptt_id"] = HODUpdateView.deptt_id
        return context

    def get_success_url(self):
        return reverse('deptt-detail-view', kwargs={'pk': HODUpdateView.deptt_id})


class HODListView(SuperRequiredMixin, ListView):
    queryset = User.objects.filter(user_type='hod')
    context_object_name = 'hods'
    template_name = "admin/hod-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # hod=self.hod.hod
        # context["department"] = hod.department
        return context


class HODDeleteView(SuperRequiredMixin, DeleteView):
    model = User
    template_name = "admin/hod-delete.html"

    def get_success_url(self):
        return reverse('deptt-list-view')

# HOD views start from here


@hod_required
def HOD_Dashboard(request):
    user = request.user.hod
    teachers = Teacher_User.objects.filter(department=user.department)
    students = Student_User.objects.filter(department=user.department)
    assigned_courses = Course.objects.filter(department=user.department, teacher__isnull=False)
    unassigned_courses = Course.objects.filter(department=user.department, teacher__isnull=True)

    # teacher_user=User.objects.filter(is_teacher=True)
    # teachers=User.teacher_user.filter(department=user.department)

    context = {
        'user': user,
        'teachers': teachers,
        'students': students,
        'assigned_courses': assigned_courses,
        'unassigned_courses': unassigned_courses,
    }

    return render(request, 'HOD/hod-dashboard.html', context)


@hod_required
def Teacher_list_View(request):
    user = request.user.hod
    teachers = Teacher_User.objects.filter(department=user.department)

    context = {
        'user': user,
        'teachers': teachers,
    }

    return render(request, 'HOD/teacher_list.html', context)


@hod_required
def Teacher_Create_View(request):

    if request.method == 'POST':
        form1 = User_Form(request.POST)
        form2 = Teacher_User_Form(request.POST)
        if form1.is_valid() and form2.is_valid():
            email = form1.cleaned_data['email']
            user = form1.save(commit=False)
            user.user_type = 'teacher'
            password = User.objects.make_random_password(
                length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")  # zvk0hawf8m6394
            user.set_password(password)

            send_mail(
                subject='Account Created',
                message='your account has been created with your email and password is '+password,
                from_email="test@gmail.com",
                recipient_list=[email, ],
                fail_silently=False,

            )
            user.save()
            teacher = form2.save(commit=False)
            teacher.teacher = user
            hod = request.user.hod.department
            teacher.department = hod
            teacher.save()
            return redirect('hod-dashboard')

    else:
        form1 = User_Form(request.POST)
        form2 = Teacher_User_Form(request.POST)

    return render(request, 'HOD/teacher-create-view.html', {'form1': form1, 'form2': form2})


@hod_required
def Teacher_Update_View(request, pk):
    user = get_object_or_404(User, id=pk)
    teacher = user.teacher_user
    if request.method == 'POST':
        form1 = User_Form(request.POST or None, instance=user)
        form2 = Teacher_User_Form(request.POST or None, instance=teacher)
        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            user.user_type = 'teacher'
            user.save()
            teacher = form2.save(commit=False)
            teacher.teacher = user
            hod = request.user.hod.department
            teacher.department = hod
            teacher.save()
            return redirect('hod-dashboard')
    else:
        form1 = User_Form(request.POST or None, instance=user)
        form2 = Teacher_User_Form(request.POST or None, instance=teacher)

    return render(request, 'HOD/teacher-create-view.html', {'form1': form1, 'form2': form2})


@hod_required
def Teacher_delete_View(request, pk):
    user = get_object_or_404(User, id=pk)
    user.delete()
    return redirect('hod-dashboard')


@hod_required
def Batch_list(request):
    department = request.user.hod.department
    batches = Batch.objects.filter(department=department)
    semesters = Semester.objects.filter(department=department)
    return render(request, 'HOD/batch-list.html', context={'department': department, 'batches': batches, 'semesters': semesters})


@hod_required
def Batch_detail(request, pk):
    department = request.user.hod.department
    batch = get_object_or_404(Batch, id=pk, department=department)
    batch = get_object_or_404(Batch, id=pk, department=department)
    students = Student_User.objects.filter(
        batch=batch, department=department)
    return render(request, 'HOD/batch_detail.html', context={
        'department': department,
        'batch': batch,
        'students': students,
    })
        


@hod_required
def Batch_Create_View(request):

    if request.method == 'POST':
        form = Batch_Create_Form(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.department = request.user.hod.department
            form.save()
            return redirect('batch-list-view')
    else:
        form = Batch_Create_Form()

    return render(request, 'HOD/batch-create-view.html', {'form': form, })


@hod_required
def Batch_Update_View(request,pk):
    department = request.user.hod.department
    batch = get_object_or_404(Batch, id=pk, department=department)
    if request.method == 'POST':
        form = Batch_Create_Form(request.POST or None, instance=batch)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('batch-list-view')
    else:
        form = Batch_Create_Form(request.POST or None, instance=batch)

    return render(request, 'HOD/batch-create-view.html', {'form': form, })


@hod_required
def Batch_delete_View(request, pk):
    batch = get_object_or_404(Batch, id=pk)
    batch.delete()
    return redirect('batch-list-view')


class Semester_Create_View(HODRequiredMixin,CreateView):
    form_class = Semester_Create_Form
    template_name = "HOD/batch-create-view.html"

    def get_success_url(self):
        return reverse('batch-list-view')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(Semester_Create_View, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        semester = form.save(commit=False)
        semester.department = self.request.user.hod.department
        semester.save()
        return super().form_valid(form)
class Semester_Update_View(HODRequiredMixin,UpdateView):
    form_class = Semester_Create_Form
    model=Semester
    template_name = "HOD/batch-create-view.html"

    def get_success_url(self):
        
        return reverse('semester_detail', args=(self.kwargs.get('pk')),)

    def get_form_kwargs(self):
        kwargs = super(Semester_Update_View, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@hod_required
def Semester_detail(request, pk):
    department = request.user.hod.department
    semester = get_object_or_404(Semester, id=pk,department=department)
    

    return render(request, 'HOD/Semester-detail.html', context={'semester': semester,})


@hod_required
def Semester_delete(request,pk):
    department = request.user.hod.department
    semester = get_object_or_404(Semester, id=pk,department=department)
    semester.delete()
    return redirect('batch-list-view')


@hod_required
def Course_Create_View(request,):
    if request.method == 'POST':
        form = Course_Create_Form(request.POST)

        if form.is_valid():
            departement = request.user.hod.department
            courses = Course.objects.filter(department=departement)
            course = form.save(commit=False)
            for c in courses:
                if c.subject_name.lower() == course.subject_name.lower() :
                    messages.info(
                        request, f'A subject with the name {c} already exist.')
                    return redirect('course_create_view')
            course.department = departement
            course.save()
            return redirect('hod-dashboard')
                
    else:
        form = Course_Create_Form()
    return render(request, 'HOD/batch-create-view.html', context={'form': form, })


@hod_required
def Course_Update_View(request, pk):
    department = request.user.hod.department
    course=get_object_or_404(Course,id=pk,department=department)
    if request.method == 'POST':
        form = Course_Create_Form(request.POST or None, instance=course)

        if form.is_valid():
            departement = request.user.hod.department
            courses = Course.objects.filter(department=departement)
            course = form.save(commit=False)
            for c in courses:
                if c.subject_name.lower() == course.subject_name.lower():
                    messages.info(
                        request, f'A subject with the name {c} already exist.')
                    return redirect('course_update_view',id=pk)
            course.save()
            return redirect('hod-dashboard')
                
    else:
        form = Course_Create_Form(request.POST or None, instance=course)
    return render(request, 'HOD/batch-create-view.html', context={'form': form, })

    # def form_valid(self, form):
    #     """If the form is valid, save the associated model."""
    #     semester = form.save(commit=False)
    #     semester.department = self.request.user.hod.department
    #     semester.save()
    #     return super().form_valid(form)


@hod_required
def Course_Delete_View(request,pk):
    department = request.user.hod.department
    course = get_object_or_404(Course, id=pk, department=department)
    course.delete()
    return redirect('hod-dashboard')


@hod_required
def Student_Create_View(request, pk):

    if request.method == 'POST':
        form1 = User_Form(request.POST)
        form2 = Student_Create_Form(request.POST)
        if form1.is_valid() and form2.is_valid():
            email = form1.cleaned_data['email']
            user = form1.save(commit=False)
            user.user_type = 'student'
            password = User.objects.make_random_password(
                length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")  # zvk0hawf8m6394
            user.set_password(password)

            send_mail(
                subject='Account Created',
                message='your account has been created with your email and password is '+password,
                from_email="test@gmail.com",
                recipient_list=[email, ],
                fail_silently=False,

            )
            user.save()
            student = form2.save(commit=False)
            student.student = user
            hod = request.user.hod.department
            student.department = hod
            batch = get_object_or_404(Batch, id=pk)
            print(batch, hod, student.roll_no)
            student.batch = batch
            student.save()
            return redirect('batch_detail', pk=pk)

    else:
        form1 = User_Form()
        form2 = Student_Create_Form()

    return render(request, 'HOD/teacher-create-view.html', {'form1': form1, 'form2': form2})


@hod_required
def Student_Update_View(request, pk):
    user = get_object_or_404(User, id=pk)
    department = request.user.hod.department
    student = user.student_user
    student_department=student.department
    print(student_department)
    if department == student_department:
        if request.method == 'POST':
            form1 = User_Form(request.POST or None, instance=user)
            form2 = Student_Create_Form(request.POST or None, instance=student)
            if form1.is_valid() and form2.is_valid():
                email = form1.cleaned_data['email']
                user = form1.save(commit=False)
                user.save()
                student = form2.save(commit=False)
                student.student = user
                student.save()
                return redirect('batch_detail', pk=student.batch.id)

        else:
            form1 = User_Form(request.POST or None, instance=user)
            form2 = Student_Create_Form(request.POST or None, instance=student)
        return render(request, 'HOD/teacher-create-view.html', {'form1': form1, 'form2': form2})
    else:
        return redirect('batch-list-view')


@hod_required
def Student_delete_View(request, pk):
    user = get_object_or_404(User, id=pk)
    student = user.student_user.batch.id
    department = request.user.hod.department
    student = user.student_user
    student_department = student.department
    if department==student_department:
        user.delete()
        return redirect('batch_detail', pk=student)
    else:
        return redirect('batch-list-view')


# Teachers dashboard



# def Teacher_dashboard(request):
#     assigned_courses = Course.objects.filter(
#         teacher=request.user.teacher_user)
#     context = {'assigned_courses': assigned_courses}
#     return render(request,'teacher/dashboard.html',context)

# def Teacher_Course_Detail(request,pk):
#     course=get_object_or_404(Course,id=pk,department=request.user.teacher_user.department)
#     context={
#         'course':course,
#     }
#     return render(request, 'teacher/teacher_course_detail.html', context)

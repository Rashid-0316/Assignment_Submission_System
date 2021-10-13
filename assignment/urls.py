from django.urls import path
from .views import *



urlpatterns = [

    path('',LandingPage.as_view(),name='landing-page'),

    #Admin urls
    path('deptt-list-view/',DepttListView.as_view(),name='deptt-list-view'),
    path('deptt-create-view/',DepttCreateView.as_view(),name='deptt-create-view'),    
    path('deptt-update-view/<int:pk>',DepttUpdateView.as_view(),name='deptt-update-view'),
    path('deptt-detail-view/<int:pk>/',DepttDetailView.as_view(),name='deptt-detail-view'),
    path('deptt-delete-view/<int:pk>/',DepttDeleteView.as_view(),name='deptt-delete-view'),
    path('hod-create-view/',HODCreateView.as_view(),name='hod-create-view'),
    path('hod-update-view/<int:pk>/',HODUpdateView.as_view(),name='hod-update-view'),
    path('hod-delete-view/<int:pk>/',HODDeleteView.as_view(),name='hod-delete-view'),
    path('hod-list-view/',HODListView.as_view(),name='hod-list-view'),


    # hod urls
    path('hod-dashboard/',HOD_Dashboard,name='hod-dashboard'),
    path('teacher-list-view/',Teacher_list_View,name='teacher-list-view'),
    path('teacher-create-view/',Teacher_Create_View,name='teacher-create-view'),
    path('teacher-update-view/<str:pk>',Teacher_Update_View,name='teacher-update-view'),
    path('teacher-delete-view/<str:pk>',Teacher_delete_View,name='teacher-delete-view'),
    path('batch-list-view/',Batch_list,name='batch-list-view'),
    path('batch/<str:pk>',Batch_detail,name='batch_detail'),
    path('semester/<str:pk>',Semester_detail,name='semester_detail'),
    path('batch-create-view/',Batch_Create_View,name='batch_create_view'),
    path('batch-update-view/<str:pk>/',Batch_Update_View,name='batch_update_view'),
    path('batch-delete-view/<str:pk>/',Batch_delete_View,name='batch_delete_view'),
    path('semester-create-view/',Semester_Create_View.as_view(),name='semester_create_view'),
    path('semester-update-view/<str:pk>/',Semester_Update_View.as_view(),name='semester_update_view'),
    path('semester-delete-view/<str:pk>/',Semester_delete,name='semester_delete_view'),
    path('student-create-view/<str:pk>',Student_Create_View,name='student_create_view'),
    path('student-update-view/<str:pk>',Student_Update_View,name='student_update_view'),
    path('student-delete-view/<str:pk>',Student_delete_View,name='student_delete_view'),
    path('course-create-view/',Course_Create_View, name='course_create_view'),
    path('course-update-view/<str:pk>/',Course_Update_View, name='course_update_view'),
    path('course-delete-view/<str:pk>/',Course_Delete_View, name='course_delete_view'),

    
    #Teacher dashboard
    # path('teacher-dashboard', Teacher_dashboard, name='teacher-dashboard'),
    # path('teacher-course-detail/<str:pk>/',
    #      Teacher_Course_Detail, name='teacher-course-detail'),


]

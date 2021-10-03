from django.urls import path
from .views import *



urlpatterns = [

    path('',LandingPage.as_view(),name='landing-page'),
    path('deptt-list-view/',DepttListView.as_view(),name='deptt-list-view'),
    path('deptt-create-view/',DepttCreateView.as_view(),name='deptt-create-view'),    
    path('deptt-update-view/<int:pk>',DepttUpdateView.as_view(),name='deptt-update-view'),
    path('deptt-detail-view/<int:pk>/',DepttDetailView.as_view(),name='deptt-detail-view'),
    path('deptt-delete-view/<int:pk>/',DepttDeleteView.as_view(),name='deptt-delete-view'),
    

    path('hod-create-view/',HODCreateView.as_view(),name='hod-create-view'),
    
    path('hod-update-view/<int:pk>/',HODUpdateView.as_view(),name='hod-update-view'),
    path('hod-delete-view/<int:pk>/',HODDeleteView.as_view(),name='hod-delete-view'),
    path('hod-list-view/',HODListView.as_view(),name='hod-list-view'),


    # hod dashboard
    path('hod-dashboard/',HOD_Dashboard,name='hod-dashboard'),
    path('teacher-list-view/',Teacher_list_View,name='teacher-list-view'),
    path('teacher-create-view/',Teacher_Create_View,name='teacher-create-view'),
    path('teacher-update-view/<str:pk>',Teacher_Update_View,name='teacher-update-view'),
    path('teacher-delete-view/<str:pk>',Teacher_delete_View,name='teacher-delete-view'),

]

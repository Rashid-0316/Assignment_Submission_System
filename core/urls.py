"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from core.settings import DEBUG
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView,LogoutView,
    PasswordResetView,PasswordResetDoneView,
    PasswordResetConfirmView,PasswordResetCompleteView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('assignment.urls')),



    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    # path('signup/',SignUpView.as_view(),name='signup'),
    path('password-reset/',PasswordResetView.as_view(),name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-done/',PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),

]

if DEBUG==True:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'assignment.views.error_404'
# handler500 = 'myappname.views.error_500'
# handler403 = 'myappname.views.error_403'
# handler400 = 'myappname.views.error_400'

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('jobs/', views.search_jobs, name='search_jobs'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('post-job/', views.post_job, name='post_job'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('dashboard/seeker/', views.seeker_dashboard, name='seeker_dashboard'),
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    path('dashboard/employer/job/<int:job_id>/applications/', views.job_applications, name='job_applications'),
    path('dashboard/employer/application/<int:app_id>/update/', views.update_application_status, name='update_application_status'),
    path('dashboard/employer/job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('about/', views.about, name='about'),
]

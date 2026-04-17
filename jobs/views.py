from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Job, Application, UserProfile


# HOME PAGE
def home(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:6]
    total_jobs = Job.objects.filter(is_active=True).count()
    total_companies = Job.objects.values('company').distinct().count()
    total_users = User.objects.count()
    return render(request, 'home.html', {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'total_users': total_users,
        'categories_list': Job.CATEGORY_CHOICES,
    })


# REGISTER
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', 'job_seeker')

        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return redirect('register')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, role=role)
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    return render(request, 'register.html')


# LOGIN
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # Ensure profile exists
            UserProfile.objects.get_or_create(user=user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


# LOGOUT
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# SEARCH / BROWSE JOBS
def search_jobs(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    title = request.GET.get('title', '')
    location = request.GET.get('location', '')
    category = request.GET.get('category', '')
    company = request.GET.get('company', '')
    job_type = request.GET.get('job_type', '')

    if title:
        jobs = jobs.filter(title__icontains=title)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if category:
        jobs = jobs.filter(category=category)
    if company:
        jobs = jobs.filter(company__icontains=company)
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    categories = Job.CATEGORY_CHOICES
    job_types = Job.JOB_TYPE_CHOICES
    return render(request, 'jobs.html', {
        'jobs': jobs,
        'categories': categories,
        'job_types': job_types,
        'title': title,
        'location': location,
        'category': category,
        'company': company,
        'job_type': job_type,
    })


# JOB DETAIL
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    already_applied = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    return render(request, 'job_detail.html', {'job': job, 'already_applied': already_applied})


# POST JOB (Employer only)
@login_required(login_url='login')
def post_job(request):
    try:
        profile = request.user.profile
        if profile.role != 'employer' and not request.user.is_staff:
            messages.error(request, 'Only employers can post jobs. Please register as an employer.')
            return redirect('home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        company = request.POST.get('company', '').strip()
        location = request.POST.get('location', '').strip()
        salary = request.POST.get('salary', '').strip()
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category', 'other')
        job_type = request.POST.get('job_type', 'full_time')

        if not all([title, company, location, salary, description]):
            messages.error(request, 'All fields are required.')
            return render(request, 'post_job.html', {
                'categories': Job.CATEGORY_CHOICES,
                'job_types': Job.JOB_TYPE_CHOICES,
            })

        Job.objects.create(
            title=title, company=company, location=location,
            salary=salary, description=description,
            category=category, job_type=job_type,
            employer=request.user
        )
        messages.success(request, 'Job posted successfully!')
        return redirect('employer_dashboard')

    return render(request, 'post_job.html', {
        'categories': Job.CATEGORY_CHOICES,
        'job_types': Job.JOB_TYPE_CHOICES,
    })


# APPLY FOR JOB (Job Seekers)
@login_required(login_url='login')
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    try:
        profile = request.user.profile
        if profile.role == 'employer' and not request.user.is_staff:
            messages.error(request, 'Employers cannot apply for jobs.')
            return redirect('job_detail', job_id=job_id)
    except UserProfile.DoesNotExist:
        pass

    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job_id)

    if request.method == 'POST':
        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter', '').strip()

        if not resume:
            messages.error(request, 'Please upload your resume.')
            return redirect('job_detail', job_id=job_id)

        Application.objects.create(
            job=job,
            applicant=request.user,
            resume=resume,
            cover_letter=cover_letter
        )
        messages.success(request, f'Application submitted for {job.title}!')
        return redirect('seeker_dashboard')

    return render(request, 'apply_job.html', {'job': job})


# JOB SEEKER DASHBOARD
@login_required(login_url='login')
def seeker_dashboard(request):
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')
    return render(request, 'seeker_dashboard.html', {'applications': applications})


# EMPLOYER DASHBOARD
@login_required(login_url='login')
def employer_dashboard(request):
    try:
        profile = request.user.profile
        if profile.role != 'employer' and not request.user.is_staff:
            messages.error(request, 'Access denied.')
            return redirect('home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')

    jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    return render(request, 'employer_dashboard.html', {'jobs': jobs})


# EMPLOYER: VIEW APPLICATIONS FOR A JOB
@login_required(login_url='login')
def job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = job.applications.all().order_by('-applied_at')
    return render(request, 'job_applications.html', {'job': job, 'applications': applications})


# EMPLOYER: UPDATE APPLICATION STATUS
@login_required(login_url='login')
def update_application_status(request, app_id):
    application = get_object_or_404(Application, id=app_id, job__employer=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'reviewed', 'accepted', 'rejected']:
            application.status = new_status
            application.save()
            messages.success(request, 'Application status updated.')
    return redirect('job_applications', job_id=application.job.id)


# EMPLOYER: DELETE JOB
@login_required(login_url='login')
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job listing deleted.')
    return redirect('employer_dashboard')


# ABOUT
def about(request):
    return render(request, 'about.html')


# Context processor helper — update home view to include categories
# (Override home with categories_list)

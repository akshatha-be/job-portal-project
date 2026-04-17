from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Job(models.Model):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('design', 'Design'),
        ('sales', 'Sales'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('engineering', 'Engineering'),
        ('other', 'Other'),
    ]
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    salary = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs_posted')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def application_count(self):
        return self.applications.count()


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant} applied for {self.job}"

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('job_seeker', 'Job Seeker'), ('employer', 'Employer')], default='job_seeker', max_length=20)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('bio', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('salary', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('technology', 'Technology'), ('finance', 'Finance'), ('marketing', 'Marketing'), ('design', 'Design'), ('sales', 'Sales'), ('healthcare', 'Healthcare'), ('education', 'Education'), ('engineering', 'Engineering'), ('other', 'Other')], default='other', max_length=50)),
                ('job_type', models.CharField(choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('contract', 'Contract'), ('internship', 'Internship'), ('remote', 'Remote')], default='full_time', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs_posted', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(upload_to='resumes/')),
                ('cover_letter', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobs.job')),
            ],
            options={
                'unique_together': {('job', 'applicant')},
            },
        ),
    ]

# JobVerse — Professional Job Portal

## Features
- **3 User Roles**: Job Seeker, Employer, Admin
- **Job Seekers**: Register, search & filter jobs, apply with resume upload, track applications
- **Employers**: Post jobs with category/type, manage listings, review & update applications
- **Admin**: Full Django admin panel for all users, jobs, applications

## Tech Stack
- Backend: Django (Python)
- Frontend: HTML, CSS, Bootstrap 5.3
- Database: SQLite
- Icons: Bootstrap Icons

## Setup & Run

```bash
# 1. Install dependencies
pip install django

# 2. Apply migrations
python manage.py migrate

# 3. Create admin superuser
python manage.py createsuperuser

# 4. Run the server
python manage.py runserver
```

Then visit: http://127.0.0.1:8000

Admin panel: http://127.0.0.1:8000/admin


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField

class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('department1', 'Department 1'),
        ('department2', 'Department 2'),
        ('department3', 'Department 3'),
        ('department4', 'Department 4'),

    ]

    name = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class Role(models.Model):
    Roles_CHOICES = [
        ('student', 'student'),
        ('staff', 'staff'),
    ]

    name = models.CharField(max_length=50, choices=Roles_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()
    
class CustomUser(AbstractUser):
    # Add additional fields here
    STUDENT = 'student'
    STAFF = 'staff'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (STAFF, 'Staff'),
    ]
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    department = department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    country = CountryField(blank_label='(Select country)', blank=True, null=True)  # Optional field for country
    time_of_access = models.DateTimeField(default=timezone.now)

class Library(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='libraries')
    content = models.TextField()


class Course(models.Model):
    COURSE_CHOICES = [
        ('course1', 'Course 1'),
        ('course2', 'Course 2'),
        ('course3', 'Course 3'),
        ('course4', 'Course 4'),
    ]
    name = models.CharField(max_length=50, choices=COURSE_CHOICES, unique=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return f"{self.get_name_display()} ({self.department.name})"

class Exam(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="exams")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course")
    content = models.TextField()
    exam_start = models.DateTimeField()
    exam_end = models.DateTimeField()
    txt = models.CharField(max_length=1)

    def is_available(self):
        now = timezone.now()
        return self.exam_start <= now <= self.exam_end

    def __str__(self):
        return self.title



from django.conf import settings

class Materialcourse(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='course_materials/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_files')

    def __str__(self):
        return self.title


class UserLoginHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='login_history')
    timestamp = models.DateTimeField(auto_now_add=True)
    device_type = models.CharField(max_length=100)
    is_touch_capable = models.BooleanField(default=False)
    browser_family = models.CharField(max_length=100)
    browser_version = models.CharField(max_length=100)
    os_family = models.CharField(max_length=100)
    os_version = models.CharField(max_length=100)
    device_family = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username} logged in using {self.device_type} on {self.timestamp}'


##### visualss3###
import matplotlib.pyplot as plt
from django.http import HttpResponse
from .models import CustomUser, Course, Department
from django.db.models import Count

def student_count_per_department(request):
    # Query the database for student counts per department
    department_counts = CustomUser.objects.filter(role__name='student').values('department__name').annotate(count=Count('id')).order_by()

    # Create a bar chart
    plt.figure(figsize=(10, 5))
    plt.bar([item['department__name'] for item in department_counts], [item['count'] for item in department_counts], color='skyblue')
    plt.xlabel('Department')
    plt.ylabel('Number of Students')
    plt.title('Student Counts per Department')
    plt.xticks(rotation=45)
    plt.tight_layout()
    response = HttpResponse(content_type="image/png")
    plt.savefig(response, format='png')
    plt.close()
    return response

def course_distribution(request):
    # Query the database for course counts by department
    course_counts = Course.objects.values('department__name').annotate(count=Count('id'))

    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie([item['count'] for item in course_counts], labels=[item['department__name'] for item in course_counts], autopct='%1.1f%%', startangle=90)
    plt.title('Course Distribution by Department')
    response = HttpResponse(content_type="image/png")
    plt.savefig(response, format='png')
    plt.close()
    return response

from django.contrib import admin
from .models import CustomUser, Department, Role,Library,Exam,Course, Materialcourse,UserLoginHistory
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser




# Register your models here.
# admin.site.register(CustomUser)
# admin.site.register(Department)
# admin.site.register(Role)
# admin.site.register(Library)
# admin.site.register(Course)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['id','title','department','course','exam_start','exam_end']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id','username','role','department','country','time_of_access']
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['id','department','content']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','name','department']

@admin.register(Materialcourse)
class MaterialcourseAdmin(admin.ModelAdmin):
    list_display = ['id','title','pdf_file','uploaded_by']



@admin.register(UserLoginHistory)
class UserLoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['user','timestamp','device_type','browser_version','is_touch_capable','browser_family','os_family','os_version','device_family']


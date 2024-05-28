
from django.contrib import admin
from django.urls import path,include
from app import views
from app.views import CustomLoginView, otp_challenge
from app.views import UserProfileView
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('accounts/profile/',UserProfileView.as_view(), name='user_profile'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('', CustomLoginView.as_view(), name='account_login'),
    path('accounts/otp_challenge/', otp_challenge, name='otp_challenge'),
    path('profile/',UserProfileView.as_view(), name='user_profile'),
    path('accounts/library/',views.library_view, name='library-detail'),
    path('accounts/fees/',views.sensitive_data, name='sensitive_data'),
    path('admin/', admin.site.urls),
    path('accounts/two-factor/', include('allauth_2fa.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/remote_acess',views.remote_acess,name='remote_acess'),
    path('accounts/exam/<int:exam_id>/', views.view_exam, name='view_exam'),
    path('accounts/exams/all/', views.view_all_exams, name='view_all_exam'),
    path('accounts/create-exam/', views.create_exam, name='create_exam'),
    path('accounts/my_activity', views.my_activity, name='my_activity'),
    path('accounts/my_device', views.my_device, name='my_device'),
    path('accounts/upload/', views.upload_course_material, name='upload_course_material'),
    path('accounts/materials/', views.list_course_materials, name='course_materials_list'),
    path('accounts/login-history/', views.view_login_history, name='login_history'),
    path('accounts/charts/student_counts/', views.student_count_per_department, name='student_counts'),
    path('accounts/charts/course_distribution/', views.course_distribution, name='course_distribution'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



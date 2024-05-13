from django.shortcuts import render, get_object_or_404
from .models import Library, Exam
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from django.utils import timezone

#########
from allauth.account.views import LoginView as AllAuthLoginView
from django_otp.plugins.otp_email.models import EmailDevice
from django.shortcuts import redirect
from django.urls import reverse

class CustomLoginView(AllAuthLoginView):
    def form_valid(self, form):
        # First, let Allauth handle the user authentication
        response = super().form_valid(form)
        
        # Check if user is authenticated and redirect to OTP verification page
        if self.request.user.is_authenticated:
            device, created = EmailDevice.objects.get_or_create(user=self.request.user, name='default')
            device.generate_challenge()  # Always send an OTP
            return redirect(reverse('otp_challenge'))
        
        return response

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django_otp import verify_token

@login_required
def otp_challenge(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = request.user
        device = user.emaildevice_set.first()  # Simplified device retrieval
        if device and device.verify_token(otp):
            return redirect('/profile/')  # Redirect to user profile or dashboard
        else:
            return HttpResponse('Invalid OTP ', status=403)

    return render(request, 'account/otp_challenge.html')
#########

@login_required
def library_view(request):

    if not request.user.is_active:
        return HttpResponse("This account is inactive.", status=403)
    
    user_department = request.user.department
    if not user_department:
        return HttpResponse("You are not assigned to any department.", status=403)
    
    try:
        library = Library.objects.get(department=user_department)
    except Library.DoesNotExist:
        return HttpResponse("No library content available for your department.", status=404)

    return render(request, 'account/library_detail.html', {'library': library})


current_timezone = timezone.localtime(timezone.now())
@login_required
def sensitive_data(request):
    print(current_timezone)
    if request.user.is_staff:
         return render(request, 'account/fees_detail.html',{'current_timezone': current_timezone})
    else :
        return HttpResponse("Access Denied.Sensitive Data", status=403)
    

@login_required
def view_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    
    # Check if the user's department matches the exam's department
    if request.user.department != exam.department:
        return HttpResponse("<b>You are not authorized to view this exam.</b>", status=403)
    
    # Check if the current time is within the exam window
    if not exam.is_available():
        return HttpResponse("This exam is not currently available.", status=403)
    
    return render(request, 'account/exam_detail.html', {'exam': exam,'current_timezone': current_timezone,'exam_id': exam_id})

@login_required
def view_all_exams(request):
    exams = Exam.objects.all()  # Fetching all exams from the database
    current_timezone = timezone.get_current_timezone_name()  # Getting the current timezone
    context = {
        'exams': exams,
        'current_timezone': current_timezone,
    }
    return render(request, 'account/exam_list.html', context)


from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser

class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'account/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
    
def remote_acess(request):
    user = request.user
    if user.country == 'AU':
        return HttpResponse('acess not granted')
    return render(request, 'account/remote_acess.html')


from .forms import ExamForm

def create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_all_exam')
    else:
        form = ExamForm()

    return render(request, 'account/create_exam.html', {'form': form})

from allauth.usersessions.models import UserSession

@login_required
def my_activity(request):
    # Retrieve only sessions belonging to the logged-in user
    session = UserSession.objects.filter(user=request.user)
    context = {
        'session': session,
    }
    return render(request, 'account/my_activity.html', context)
    

# class UserSession(models.Model):
#     objects = UserSessionManager()

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(default=timezone.now)
#     ip = models.GenericIPAddressField()
#     last_seen_at = models.DateTimeField(default=timezone.now)
#     session_key = models.CharField(
#         _("session key"), max_length=40, unique=True, editable=False
#     )
#     user_agent = models.CharField(max_length=200)
#     data = models.JSONField(default=dict)


from django_user_agents.utils import get_user_agent

def my_device(request):
    # Extracting user agent information
    user_agent = request.user_agent

    # Device Type Analysis
    if user_agent.is_mobile:
        device_type = 'Mobile'
    elif user_agent.is_tablet:
        device_type = 'Tablet'
    elif user_agent.is_pc:
        device_type = 'Desktop'
    elif user_agent.is_bot:
        device_type = 'Bot'
    else:
        device_type = 'Unknown Device Type'

    # Checking Touch Capability
    is_touch_capable = 'Yes' if user_agent.is_touch_capable else 'No'

    # Browser Information
    browser_family = user_agent.browser.family
    browser_version = user_agent.browser.version_string

    # Operating System Information
    os_family = user_agent.os.family
    os_version = user_agent.os.version_string

    # Device Information
    device_family = user_agent.device.family

    # Prepare context to send to the template
    context = {
        'device_type': device_type,
        'is_touch_capable': is_touch_capable,
        'browser_family': browser_family,
        'browser_version': browser_version,
        'os_family': os_family,
        'os_version': os_version,
        'device_family': device_family,
    }

    return render(request, 'account/my_device.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CourseMaterialForm
from .models import Materialcourse

@login_required
def upload_course_material(request):
    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.save()
            return redirect('course_materials_list')
    else:
        form = CourseMaterialForm()
    return render(request, 'account/upload_course_material.html', {'form': form})

@login_required
def list_course_materials(request):
    materials = Materialcourse.objects.all()
    return render(request, 'account/list_course_materials.html', {'materials': materials})




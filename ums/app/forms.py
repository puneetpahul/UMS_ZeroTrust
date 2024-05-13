from django import forms
from allauth.account.forms import SignupForm
from .models import Role, Department,Exam, Materialcourse
from django_countries.fields import CountryField

class CustomSignupForm(SignupForm):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    country = CountryField().formfield(required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.role = self.cleaned_data['role']
        user.department = self.cleaned_data['department']
        user.county = self.cleaned_data['country']  # Save the location
        user.save()
        return user
    
## form to create exam

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'department', 'course', 'content', 'exam_start', 'exam_end', 'txt']
        widgets = {
            'exam_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'exam_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }


class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = Materialcourse
        fields = ['title', 'pdf_file']
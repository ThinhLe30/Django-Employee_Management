from django import forms
from .models import Employee
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        labels = {
            'firstName' : 'First Name',
            'lastName' : 'Last Name',
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeForm,self).__init__(*args, **kwargs)
        self.fields['department'].empty_label = "Select Department"
        self.fields['salary'].empty_label = "Select Salary Level"
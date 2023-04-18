from django import forms
from .models import AdminApp
class AdminForm(forms.ModelForm):
    class Meta:
        model = AdminApp
        fields = '__all__'
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

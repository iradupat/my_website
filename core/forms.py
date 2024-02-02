from django import forms

from core.models import Course

class FileUploadForm(forms.Form):
    excel_file = forms.FileField()
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
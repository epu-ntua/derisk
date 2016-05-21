from django import forms
from derisk_app.models import *


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('created_by',)

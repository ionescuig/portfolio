from django import forms
from.models import Project, Images, CV


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'position', 'link_host', 'link_github']


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']


class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = '__all__'

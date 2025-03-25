from django import forms

from .models import Task, Team

class AddTasksForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Description',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            })
        }

class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Team Name',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
    }
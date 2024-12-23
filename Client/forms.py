from django import forms
from .models import UsersideRequest


class UsersideRequestForm(forms.ModelForm):
    class Meta:
        model = UsersideRequest
        fields = '__all__'

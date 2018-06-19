from django import forms
from .models import TimeEnter


class TimeForm(forms.ModelForm):
    class Meta:
        model = TimeEnter
        fields = ('group','time_enter_morning','time_out_morning','time_enter_evening','time_out_evening','full_time')
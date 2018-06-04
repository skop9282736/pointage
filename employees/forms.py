from django import forms
from .models import Salary, GroupSalaries, GroupSalaries

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ('id_salary_finger', 'group_salary', 'first_name', 'last_name', 'date_joined')

class GroupForm(forms.ModelForm):
    class Meta:
        model = GroupSalaries
        fields = ( 'name',)
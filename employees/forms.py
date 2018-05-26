from django import forms
from .models import Salary, GroupSalaries

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ('id_salary_finger', 'group_salary', 'first_name', 'last_name', 'date_joined')

    id_salary_finger  = forms.CharField(
            widget=forms.TextInput(
                    attrs={"class": "form-control",
                      "placeholder": "L'identifiant que vous lui avez donné dans l'empreinte digitale"}),label='ID employe empreinte')
    first_name  = forms.CharField(
            widget=forms.TextInput(
                    attrs={"class": "form-control",
                      "placeholder": "Prénom"}),label='Prénom')
    last_name  = forms.CharField(
            widget=forms.TextInput(
                    attrs={"class": "form-control",
                      "placeholder": "Nom"}),label='Nom')
    # picture  = forms.ImageField(label='Image')




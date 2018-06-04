from rest_framework import serializers
from .models import Salary, GroupSalaries


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model =  GroupSalaries
		fields = ('id','name',)

class SalarySerializer(serializers.ModelSerializer):
	class Meta:
		model =  Salary
		fields = ('id_salary_finger','group_salary','first_name','last_name','date_joined')


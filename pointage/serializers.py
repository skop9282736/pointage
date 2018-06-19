from rest_framework import serializers
from .models import TimeEnter
from employees.models import GroupSalaries


class TimeSerializer(serializers.ModelSerializer):
	class Meta:
		model =  TimeEnter
		fields = ('id','group','time_enter_morning','time_out_morning','time_enter_evening','time_out_evening','full_time')
		
class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model =  GroupSalaries
		fields = ('id','name',)
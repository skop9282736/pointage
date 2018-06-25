from rest_framework import serializers
from .models import TimeEnter , Break, Holidays
from employees.models import GroupSalaries, Salary 
from .pointages import set_break


class TimeSerializer(serializers.ModelSerializer):
	class Meta:
		model =  TimeEnter
		fields = ('id','group','time_enter_morning','time_out_morning','time_enter_evening','time_out_evening','full_time')
		
class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model =  GroupSalaries
		fields = ('id','name',)


class BreakSerializer(serializers.ModelSerializer):
	class Meta:
		model =  Break
		fields = ('id','salary','start','end')

class SalarySerializer(serializers.ModelSerializer):
	class Meta:
		model =  Salary
		fields = ('id','id_salary_finger','group_salary','first_name','last_name','date_joined')


class HolidaysSerializer(serializers.ModelSerializer):
	class Meta:
		model =  Holidays
		fields =('id','holiday_name','start','end')
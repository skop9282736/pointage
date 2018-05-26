from django.db import models
from django.db.models.signals import post_save
from employees.models import Salary, GroupSalaries
# Create your models here.
class TimeEnter(models.Model):
    '''
    This class is for giving the legal time to enter/out of
    job by group.
    '''
    group 				= models.OneToOneField(GroupSalaries, on_delete=models.CASCADE)
    time_enter_morning 	= models.TimeField(null=False)
    time_out_morning 	= models.TimeField(null=False)
    time_enter_evening 	= models.TimeField(null=False)
    time_out_evening 	= models.TimeField(null=False)
    permanence 			= models.BooleanField(null=False, default=True)

    def __str__(self):
        return "{} {}".format(self.group,self.permanence)


class AtdRecord(models.Model):
    # This class represents records from the fingerprint
    # The names are not respecting python style because of the fingerprint machine.
    SerialId = models.BigAutoField(primary_key=True)
    CardNo = models.ForeignKey(Salary, on_delete=models.SET_NULL, null=True) #salary id
    RecDate = models.DateField()
    RecTime = models.TimeField(max_length=255)
    dateb = models.DateTimeField(max_length=255)

    def __str__(self):
        return "{} , {} ==> {}".format(self.RecDate, self.RecTime, self.CardNo.first_name)


class Holidays(models.Model):
    holiday_name = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.holiday_name

class Break(models.Model):
	#if a salary is sick or it's he's/she's holiday
    salary = models.ForeignKey(Salary, on_delete=models.SET_NULL, null=True)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return "{} , {} ==> {}".format(self.start, self.end, self.salary)
from django.db import models
from django.db.models.signals import post_save
from employees.models import Salary, GroupSalaries
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .pointages import exists, set_time, set_status, set_hours

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
    full_time 			= models.BooleanField(null=False, default=True) # True => only 2

    def __str__(self):
        return "{} {}".format(self.group,self.full_time)


class AtdRecord(models.Model):
    # This class represents records from the fingerprint
    # The names are not respecting python style because of the fingerprint machine.
    SerialId = models.BigAutoField(primary_key=True) #auto increment
    CardNo = models.ForeignKey(Salary, on_delete=models.SET_NULL, null=True) #salary
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

class Summary(models.Model):
    salary      = models.ForeignKey(Salary, on_delete=models.CASCADE)
    in_morning  = models.TimeField(null=True)
    out_morning = models.TimeField(null=True)
    in_evening  = models.TimeField(null=True)
    out_evening = models.TimeField(null=True)
    date        = models.DateField(null=True)
    status1     = models.CharField(max_length=200,null=True)
    status2     = models.CharField(max_length=200,null=True)
    nb_hours    = models.IntegerField(null=True)
    nb_minutes  = models.IntegerField(null=True)

    def __str__(self):
        return "Sumarry for: {}".format(self.salary)




def post_save_atd_reciever(sender, instance, *args, **kwargs):
    salary      = instance.CardNo
    date        = instance.RecDate
    time        = instance.RecTime
    group       = salary.group_salary
    legal_time  = TimeEnter.objects.get(group=group)
    summary     = exists(salary, date, time, Summary)

    if summary == (-1): # not exists
        summary = (Summary(salary = salary, date=date), '-1')
        summary[0].save()

    set_time(summary[0], time, legal_time)
    set_status(summary[0], legal_time)
    set_hours(summary[0], legal_time)

post_save.connect(post_save_atd_reciever, sender=AtdRecord)


def post_save_break(sender, instance, *arg, **kwarg):
    set_break(instance, Summary)

post_save.connect(post_save_break, sender=Break)


def post_save_holiday(sender, instance, *arg, **kwarg):
    set_holiday(instance, Summary, Salary)

post_save.connect(post_save_holiday, sender=Holidays)
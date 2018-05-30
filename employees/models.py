from django.db import models

# Create your models here.
class GroupSalaries(models.Model):
    # This class divide salaries by groups ex teacher, manager, saler...
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

class Salary(models.Model):
    id_salary_finger = models.IntegerField(unique=True, null=False)
    group_salary 	 = models.ForeignKey(GroupSalaries, on_delete=models.SET_NULL, null=True)
    first_name 		 = models.CharField(max_length=255)
    last_name 		 = models.CharField(max_length=255)
    # picture 		 = models.ImageField(blank=True,null=True, default="img/salary/default.png", upload_to="img/salary")
    phone            = models.CharField(blank=True, null=True, max_length=20)
    date_joined      = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
    def get_id(self):
        return self.id
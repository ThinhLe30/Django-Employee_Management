from django.db import models
class Level_Salary(models.Model):
    basicSalary = models.FloatField()
    coefficientPay = models.FloatField()
    coefficientAllowance = models.FloatField()
    class Meta:
        db_table = "level_salaries"
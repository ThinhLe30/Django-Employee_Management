from django.db import models
class Level_Salary(models.Model):
    basicSalary = models.FloatField()
    coefficientPay = models.FloatField()
    coefficientAllowance = models.FloatField()
    def __str__(self) -> str:
        return str(self.basicSalary)
    class Meta:
        db_table = "level_salaries"
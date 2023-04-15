from django.db import models
class Department(models.Model):
    name = models.CharField(max_length=45)
    address = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=45)
    description = models.CharField(max_length=500)
    def __str__(self) -> str:
        return self.name
    class Meta:
        db_table = "departments"
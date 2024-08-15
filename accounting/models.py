from django.db import models


class Payments(models.Model):
    studentName = models.CharField(max_length=30)
    studentId = models.CharField(max_length=6)
    paymentDate = models.DateField()
    level = models.CharField(max_length=5)
    amount = models.FloatField()

    def __str__(self):
        return self.studentName


class Expenses(models.Model):
    date = models.DateField()
    fuel = models.FloatField()
    stationery = models.FloatField()
    bills = models.FloatField()
    salaries = models.FloatField()

    def __str__(self):
        return self.date.strftime("%d/%m/%Y")

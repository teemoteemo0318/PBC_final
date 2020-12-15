from django.db import models
# Create your models here.


class Stock(models.Model):
    company = models.CharField(max_length=50)
    date = models.DateField()
    open = models.FloatField(max_length=50)
    high = models.FloatField(max_length=50)
    low = models.FloatField(max_length=50)
    close = models.FloatField(max_length=50)
    volume = models.FloatField(max_length=50)

    def __str__(self):
        return str(self.date) + ' ' + self.company
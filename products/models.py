from django.db import models
# Create your models here.

# 建立自己的股票資料庫
# (更新)改成使用API，因此不會用到這個model
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
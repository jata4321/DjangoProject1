from django.db import models

# Create your models here.
class Bond(models.Model):
    name = models.CharField(max_length=100)
    maturity = models.DateField()
    coupon = models.FloatField()
    def __str__(self):
        return self.name
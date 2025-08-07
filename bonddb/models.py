from datetime import date, timedelta

from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class Bond(models.Model):
    name = models.CharField(max_length=20, unique=True)
    isin = models.CharField(max_length=12, unique=True)
    coupon_rate = models.DecimalField(max_digits=7, decimal_places=4)
    coupon_frequency = models.PositiveSmallIntegerField(default=1, verbose_name='Coupon Frequency (times per year)')
    maturity_date = models.DateField(validators=[MinValueValidator(limit_value=date.today() + timedelta(days=1))])
    redemption_price = models.DecimalField(max_digits=7, decimal_places=4)
    currency = models.CharField(max_length=3)
    has_call_option = models.BooleanField(default=False)
    call_price = models.DecimalField(max_digits=7, decimal_places=4)
    call_date = models.DateField(verbose_name='Call Date')
    description = models.TextField(max_length=1000, blank=True, null=True)

    def clean(self):
        if not self.has_call_option:
            self.call_date = self.maturity_date
            self.call_price = 100

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['maturity_date']
        verbose_name = 'Bond'
        verbose_name_plural = 'Bonds'
        unique_together = ('name', 'isin')
        app_label = 'bonddb'

    def __str__(self):
        return self.name
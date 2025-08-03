from django.db import models
from django.db.models import TextChoices


# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.country_name

class Type(models.Model):

    class Currency(TextChoices):
        PLN = 'PLN', 'PLN'
        USD = 'USD', 'USD'
        EUR = 'EUR', 'EUR'
        GBP = 'GBP', 'GBP'
        CAD = 'CAD', 'CAD'
        AUD = 'AUD', 'AUD'
        JPY = 'JPY', 'JPY'
        CHF = 'CHF', 'CHF'
        CNY = 'CNY', 'CNY'
        SEK = 'SEK', 'SEK'
        NZD = 'NZD', 'NZD'

    class Type(TextChoices):
        GOVERNMENT = 'GOVT', 'GOVT'
        SWAP = 'SWAP', 'SWAP'
        CORPORATION = 'CORP', 'CORP'

    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country')
    type_name = models.TextField(max_length=20, choices=Type, default=Type.GOVERNMENT)
    description = models.TextField(null=True, blank=True)
    iso_code = models.CharField(max_length=3, choices=Currency, default=Currency.PLN)
    currency = models.CharField(max_length=3)

    class Meta:
        unique_together = ('type_name', 'iso_code', 'currency')

    def __str__(self):
        return str(self.country) + " " + str(self.type_name)


class Tenor(models.Model):
    type_name = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='tenors')
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    tenor_6m = models.FloatField(max_length=7, null=True, blank=True)
    tenor_1y = models.FloatField(max_length=7, null=True, blank=True)
    tenor_2y = models.FloatField(max_length=7, null=True, blank=True)
    tenor_5y = models.FloatField(max_length=7, null=True, blank=True)
    tenor_7y = models.FloatField(max_length=7, null=True, blank=True)
    tenor_10y = models.FloatField(max_length=7, null=True, blank=True)

    def __str__(self):
        return str(self.type_name) + " " + str(self.date)
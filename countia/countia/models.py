from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

def one_month_from_now():
    return datetime.now() + timedelta(days=30)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()

class currenceyOptions(models.TextChoices):
    DOLLAR = 'USD', _('Dollar')
    EURO = 'EUR', _('Euro')
    YUAN = 'CNY', _('Yuan')
    YEN = 'JPY', _('Yen')
    POUND = 'GBP', _('Pound')



class Budget(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(
        max_length=3,
        choices=currenceyOptions.choices,
        default=currenceyOptions.DOLLAR
    )
    amount = models.FloatField()

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('category'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')


class Record(models.Model):
    class RecordType(models.TextChoices):
        INCREASE = 'INC', _('Increase')
        DECREASE = 'DEC', _('Decrease')

    account = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    type = models.CharField(
        max_length=3, 
        choices=RecordType.choices,
        default=RecordType.DECREASE,
    )
    currency = models.CharField(
        max_length=3,
        choices=currenceyOptions.choices,
        default=currenceyOptions.DOLLAR
    )
    time = models.TimeField(default=datetime.now, blank=True)
    amount = models.FloatField()
    description = models.CharField(blank=True, null=True, verbose_name=_('description'))
    

class RecurringRecord(Record):
    is_infinite = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    repetition_dates = ArrayField(models.IntegerField())
    end_date = models.TimeField(default=one_month_from_now)
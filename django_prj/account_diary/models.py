from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)


class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)


class Industry(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)


class Store(models.Model):
    name = models.CharField(max_length=16)
    city = models.ForeignKey(City, null=False, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, null=False, on_delete=models.CASCADE)
    industry_type = models.ForeignKey(Industry, null=False, on_delete=models.CASCADE)


class AccountDiary(models.Model):
    TYPE_CHOICES = (
        ('IN', '수입'),
        ('EX', '지출'),
    )

    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    title = models.CharField(max_length=16)

    date = models.DateTimeField()

    store = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)

    type = models.CharField(max_length=2, choices=TYPE_CHOICES)

    account_tag = models.CharField(max_length=16)

    amount = models.IntegerField(default=0)

    is_public = models.BooleanField()

    description = models.TextField(max_length=1000)
    head_image = models.ImageField(upload_to='account-diary/images/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.author} :: {self.author}'

    def get_absolute_url(self):
        return f'/account-diary/{self.pk}'

# Create your models here.

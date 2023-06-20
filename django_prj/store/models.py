from django.db import models


class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.name}'


class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.name}'


class Industry(models.Model):
    id = models.CharField(primary_key=True, max_length=1)
    name = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.name}'


class Store(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)
    city = models.ForeignKey(City, null=False, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, null=False, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, null=False, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f'/store/{self.id}'

    def __str__(self):
        return f'{self.name} :: {self.country.name}'
# Create your models here.

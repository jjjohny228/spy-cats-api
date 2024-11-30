import json
import requests

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible



@deconstructible
class CatsBreedValidator:
    """
    A validator class for checking cats breed using Cats api.

    """

    def __call__(self, value: str) -> None:
        response = requests.get(f'https://api.thecatapi.com/v1/breeds/search?q={value}')
        if response.status_code == 200:
            cat_breed = response.json()
            if not cat_breed:
                raise ValidationError(f'You entered wrong cat breed')
        else:
            raise ValidationError(f'Cats api returned {response.status_code} status code')


class Cat(models.Model):
    name = models.CharField(max_length=100)
    experience = models.IntegerField()
    breed = models.CharField(max_length=100, validators=[CatsBreedValidator()])
    salary = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return self.name


class Mission(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.PROTECT, related_name='missions',  null=True, blank=True)
    complete_state = models.BooleanField(default=False)


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='targets')
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField()
    complete_state = models.BooleanField(default=False)

    def __str__(self):
        return self.name

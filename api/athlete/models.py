from django.db import models

from country.models import Country


class Athlete_Bio(models.Model):
    athlete_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=10)
    born = models.TextField()
    height = models.FloatField()
    weight = models.FloatField()
    country_noc = models.ForeignKey(Country, on_delete=models.RESTRICT)
    # country_noc = models.TextField()
    description = models.TextField()
    special_notes = models.TextField()
    country = models.TextField(default='Unknown')

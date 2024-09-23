from django.db import models

class Country(models.Model):
    noc = models.CharField(max_length=3, primary_key=True)
    country = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.country
    
class Game(models.Model):
    edition = models.CharField(max_length=255)
    edition_id = models.AutoField(primary_key=True)
    edition_url = models.CharField(max_length=255)
    year = models.IntegerField()
    city = models.CharField(max_length=100)
    country_flag_url = models.CharField(max_length=255)
    country_noc = models.ForeignKey(Country, on_delete=models.RESTRICT)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_held = models.BooleanField()
    competition_start_date = models.DateField(null=True, blank=True)
    competition_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.edition
    
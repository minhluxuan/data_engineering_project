from django.db import models

from country.models import Country, Game


class MedalTable(models.Model):
    edition_id = models.ForeignKey(Game, on_delete=models.RESTRICT)
    country_noc = models.ForeignKey(Country, on_delete=models.RESTRICT)
    gold = models.IntegerField()
    silver = models.IntegerField()
    bronze = models.IntegerField()

    def __str__(self):
        return self.country_noc + ", " + self.year + ".Gold: " + self.gold + ", Silver: " + self.silver + ", Bronze: " + self.bronze

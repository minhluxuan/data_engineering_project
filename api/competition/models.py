from django.db import models

from country.models import Country, Game


class MedalTable(models.Model):
    edition_id = models.ForeignKey(Game, on_delete=models.RESTRICT)
    country_noc = models.ForeignKey(Country, on_delete=models.RESTRICT)
    sport = models.CharField(max_length=255)
    event = models.CharField(max_length=255)
    result_id = models.ForeignKey(Result, on_delete=models.RESTRICT)
    athlete_id = models.ForeignKey(Athlete_Bio, on_delete=models.RESTRICT)
    pos = models.CharField(max_length=255)
    isTeamSport = models.BooleanField()

    def __str__(self):
        return self.event


class MedalResult(models.Model):
    edition_id = models.ForeignKey(Game, on_delete=models.RESTRICT)
    country_noc = models.ForeignKey(Country, on_delete=models.RESTRICT)
    result_id = models.ForeignKey(Result, on_delete=models.RESTRICT)
    athlete_id = models.ForeignKey(Athlete_Bio, on_delete=models.RESTRICT)
    medal = models.CharField(max_length=255)

    def __str__(self):
        return self.medal + " - " + self.athlete_id + " (" + self.country_noc + ")"


class GamesMedalTally(models.Model):
    edition_id = models.ForeignKey(Game, on_delete=models.RESTRICT)
    year = models.IntegerField()
    country_noc = models.ForeignKey(Country, on_delete=models.RESTRICT)
    gold = models.IntegerField()
    silver = models.IntegerField()
    bronze = models.IntegerField()

    def __str__(self):
        return self.country_noc + ", " + self.year + ".Gold: " + self.gold + ", Silver: " + self.silver + ", Bronze: " + self.bronze

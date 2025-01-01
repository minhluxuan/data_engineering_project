from django.db import models
from athlete.models import Athlete_Bio
from country.models import Country, Game


from athlete.models import Athlete_Bio
from country.models import Country, Game


class Result(models.Model):
    result_id = models.IntegerField(primary_key=True)
    event_title = models.CharField(max_length=255)
    edition_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    sport = models.CharField(max_length=255)
    sport_url = models.CharField(max_length=255)
    result_location = models.CharField(max_length=255)
    result_participants = models.IntegerField()
    result_countries = models.IntegerField()
    result_format = models.TextField(null=True)
    result_detail = models.TextField(null=True)
    result_description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return self.sport + '(' + self.event_title + ')'


class EventResult(models.Model):
    result_id = models.ForeignKey(Result, on_delete=models.CASCADE)
    athlete_id = models.ForeignKey(Athlete_Bio, on_delete=models.CASCADE)
    pos = models.CharField(max_length=50)
    isTeamSport = models.IntegerField()

    # def __str__(self):
    #     return str(self.athlete_id.athlete_id)


class MedalResult(models.Model):
    result_id = models.ForeignKey(Result, on_delete=models.CASCADE)
    athlete_id = models.ForeignKey(Athlete_Bio, on_delete=models.CASCADE)
    medal = models.CharField(max_length=10)

    def __str__(self):
        return self.medal + " - " + self.athlete_id + " (" + self.country_noc + ")"


class MedalTable(models.Model):
    edition_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    country_noc = models.ForeignKey(Country, on_delete=models.CASCADE)
    gold = models.IntegerField()
    silver = models.IntegerField()
    bronze = models.IntegerField()

    def __str__(self):
        return self.country_noc + ", " + self.year + ".Gold: " + self.gold + ", Silver: " + self.silver + ", Bronze: " + self.bronze

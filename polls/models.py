from django.db import models
from datetime import datetime

class Exchanges(models.Model):
    #global name1, name2, club1, club2, breakfast, lunch, dinner, month
    name1       = models.CharField(max_length=30)
    club1       = models.CharField(max_length=30)
    name2       = models.CharField(max_length=30)
    club2       = models.CharField(max_length=30)

    breakfast   = models.IntegerField(default=0)
    lunch       = models.IntegerField(default=0)
    dinner      = models.IntegerField(default=0)

    #month       = models.DateTimeField('month').now().month
    month       = models.DateTimeField(default = datetime.now().month)

    def __unicode__(self):              # __unicode__ on Python 2
        return "%s\t%s\t%s\t%s\t%d\t%d\t%d\t%d"%(self.name1, self.club1, self.name2, self.club2, self.breakfast, self.lunch, self.dinner, self.month.month)


class Members(models.Model):
    name        = models.CharField(max_length=30)
    club        = models.CharField(max_length=30)
    year        = models.IntegerField(default=0)
    netID       = models.CharField(max_length=30)
    numguests   = models.IntegerField(default=0)

    def __unicode__(self):              # __unicode__ on Python 2
        return "%s\t%s\t%d\t%s\t%d"%(self.name, self.club, self.year, self.netID, self.numguests)

class ClubPrefs(models.Model):

    b_start         = models.TimeField(default="00:00")
    l_start         = models.TimeField(default="00:00")
    d_start         = models.TimeField(default="00:00")
    b_end           = models.TimeField(default="00:00")
    l_end           = models.TimeField(default="00:00")
    d_end           = models.TimeField(default="00:00")
    br_start         = models.TimeField(default="00:00")
    br_end           = models.TimeField(default="00:00")

    max_guests   = models.IntegerField(default=0)

    def __unicode__(self):              # __unicode__ on Python 2
        return "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\%d"%(self.club_name, str(self.b_start), str(self.b_end), str(self.l_start), str(self.l_end), str(self.d_start), str(self.d_end), str(self.br_start), str(self.br_end), self.max_guests)
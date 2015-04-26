from polls.models import Exchanges, Members, ClubPrefs
from datetime import datetime

ClubPrefs.objects.all()
c = ClubPrefs(club = 'terr', btime = '0:00', ltime = '3:00', dtime = '5:00', maxguests = 0)

Exchanges.objects.all()
a = Exchanges(name1 = 'Louis', name2 = 'Louis2', club1 = 'terr', club2 = 'terr2', month = datetime.now())
a.save()
Exchanges.objects.all()

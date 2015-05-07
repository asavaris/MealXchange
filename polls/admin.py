from django.contrib import admin

from .models import Exchanges, Members, ClubPrefs, ConfirmExchange, ConfirmGuest

admin.site.register(Exchanges)
admin.site.register(Members)
admin.site.register(ClubPrefs)
admin.site.register(ConfirmExchange)
admin.site.register(ConfirmGuest)

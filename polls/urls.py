from django.conf.urls import url

from . import views

#r'^(?P<ticket>.+)/$'
#'^(?P<question_id>[0-9]+)/$'

urlpatterns = [
	url(r'^(?i)LogIn/$', views.LogIn, name='LogIn'),
	url(r'^(?i)Home/$', views.Home, name='Home'),
	url(r'^(?i)Exchange/$', views.Exchange, name='Exchange'),
	url(r'^(?i)Guest/$', views.Guest, name='Guest'),
	url(r'^(?i)Thanks/$', views.Thanks, name='Thanks'),
	url(r'^(?i)LoggedOut/$', views.LoggedOut, name='LoggedOut'),
	url(r'^(?i)Error/$', views.Error, name='Error'),
	# url(r'^(?i)Exchange/Thanks/$', views.ExchangeThanks, name='ExchangeThanks'),
	# url(r'^(?i)Guest/Thanks/$', views.GuestThanks, name='GuestThanks'),
    url(r'^(?i)ViewExchanges/$', views.ViewExchanges, name='ViewExchanges'),
    url(r'^(?i)ClubPrefs/$', views.handleClubPrefs, name='handleClubPrefs'),
    url(r'^(?i)SavedChanges/$', views.SavedChanges, name='SavedChanges'), 
    url(r'^(?i)EditMembership/$', views.EditMembership, name='EditMembership'),
    url(r'^(?i)AddMembers/$', views.AddMembers, name='AddMembers'),
    url(r'^(?i)$', views.HomeRedirect, name='HomeRedirect'),
    url(r'^(?i)Confirmation/(?P<anystring>.+)$', views.Confirmation, name='Confirmation'),
    url(r'^(?i)Download/$', views.DownloadLink, name='DownloadLink'),
    url(r'^(?i)SendEmails/$', views.SendEmails, name='SendEmails'),
    url(r'^(?i)GuestConfirmation/(?P<anystring>.+)$', views.GuestConfirmation, name='GuestConfirmation'),



]





# 	url(r'^HostLogIn/$', views.HostLogIn, name='HostLogIn'),
    # url(r'^SearchExchanges$', views.SearchExchanges, name='SearchExchanges'), 

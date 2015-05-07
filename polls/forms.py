from django import forms
from django.contrib.auth.forms import AuthenticationForm
from time import strftime
from datetime import datetime


class AuthenticationForm(forms.Form):
    id_username = forms.CharField(label='Club name', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Club Name'}))
    id_password = forms.CharField(label='Club password', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Club Password'}))

class ExchangeForm(forms.Form):
    host_name = forms.CharField(label='Host netid', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Host NetID'}))
    guest_name = forms.CharField(label='Guest netid', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Guest NetID'}))

class GuestForm(forms.Form):
    host_name = forms.CharField(label='Host netid', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Host NetID'}))

class ClubPrefsForm(forms.Form):

	def __init__(self, *args, **kwargs):
		oldPrefs = kwargs.pop('oldPrefs')

		if (oldPrefs == "null"):

			print "why is it null"
			b_start = forms.ChoiceField(timefields, label='Breakfast start time', required=True)
			b_end = forms.ChoiceField(timefields, label='Breakfast end time', required=True)
			l_start = forms.ChoiceField(timefields, label='Lunch start time', required=True)
			l_end = forms.ChoiceField(timefields, label='Lunch end time', required=True)
			d_start = forms.ChoiceField(timefields, label='Dinner start time', required=True)
			d_end = forms.ChoiceField(timefields, label='Dinner end time', required=True)
			br_start = forms.ChoiceField(timefields, label='Brunch start time', required=True)
			br_end = forms.ChoiceField(timefields, label='Brunch end time', required=True)

			max_guests = forms.IntegerField(label="Maximum number of guests", required = True, widget=forms.NumberInput(attrs={'style': 'width:62px; height:25px;'}), initial=oldPrefs.max_guests)

		else:

			print "we're loading old values"
			print "old prefs: " + str(oldPrefs)
			super(ClubPrefsForm, self).__init__(*args, **kwargs)

			timefields = [(" "," "), ("06:00","06:00"), ("06:30","06:30"), ("07:00","07:00"), ("07:30", "07:30"), ("08:00","08:00"), ("08:30", "08:30"), ("09:00", "09:00"), ("09:30", "09:30"), ("10:00","10:00"), ("10:30","10:30"), ("11:00","11:00"), ("11:30", "11:30"), ("12:00","12:00"), ("12:30", "12:30"), ("13:00", "13:00"), ("13:30", "13:30"), ("14:00","14:00"), ("14:30","14:30"), ("15:00","15:00"), ("15:30", "15:30"), ("16:00","16:00"), ("16:30", "16:30"), ("17:00", "17:00"), ("17:30", "17:30"), ("18:00","18:00"), ("18:30","18:30"), ("19:00","19:00"), ("19:30", "19:30"), ("20:00","20:00"), ("20:30", "20:30"), ("21:00", "21:00"), ("21:30", "21:30")]
			#club_name = forms.CharField(label='club name', max_length=100, required=False)
			print ("type of hour :" + str(type(oldPrefs.b_start.hour)))
			print ("type of minute: " + str(type(oldPrefs.b_start.minute)))

			print "strf thing: " + str(oldPrefs.b_start.strftime('%H:%M'))
			


			self.fields['b_start'] = forms.ChoiceField(timefields, label='Breakfast start time', required=True, initial=oldPrefs.b_start.strftime('%H:%M'))
			self.fields['b_end'] = forms.ChoiceField(timefields, label='Breakfast end time', required=True, initial=oldPrefs.b_end.strftime('%H:%M'))
			self.fields['l_start'] = forms.ChoiceField(timefields, label='Lunch start time', required=True, initial=oldPrefs.l_start.strftime('%H:%M'))
			self.fields['l_end'] = forms.ChoiceField(timefields, label='Lunch end time', required=True, initial=oldPrefs.l_end.strftime('%H:%M'))
			self.fields['d_start'] = forms.ChoiceField(timefields, label='Dinner start time', required=True, initial=oldPrefs.d_start.strftime('%H:%M'))
			self.fields['d_end'] = forms.ChoiceField(timefields, label='Dinner end time', required=True, initial=oldPrefs.d_end.strftime('%H:%M'))
			self.fields['br_start'] = forms.ChoiceField(timefields, label='Brunch start time', required=True, initial=oldPrefs.br_start.strftime('%H:%M'))
			self.fields['br_end'] = forms.ChoiceField(timefields, label='Brunch end time', required=True, initial=oldPrefs.br_end.strftime('%H:%M'))

			self.fields['max_guests'] = forms.IntegerField(label="Maximum number of guests", required = True, widget=forms.NumberInput(attrs={'style': 'width:62px; height:25px;'}), initial=oldPrefs.max_guests)

class ViewExchangesForm(forms.Form):
	# ll = forms.BooleanField(label='Member netid', required=False)
    netid = forms.CharField(label='Member netid', max_length = 20, required=False)


class ViewMembersForm(forms.Form):
	# ll = forms.BooleanField(label='Member netid', required=False)
    match = forms.CharField(label='Member netid', max_length = 20, required=False)

class EditMembershipForm(forms.Form):
	netid = forms.CharField(label='Member netid', max_length = 20, required=True, initial="NetID")
	name = 	forms.CharField(label='Member name', max_length = 20, required=True, initial="Name")
	year = forms.IntegerField(label="Member year", required = True, initial=2016)

class AddMembersForm(forms.Form):
	names = forms.CharField(label='Names (Comma Separated)', max_length = 4000,
		widget=forms.Textarea(attrs={'placeholder': 'name1, name2, etc.', 'style': 'width:400px; height:100px;font-size: 15px'}),required = True)
	netIDs = forms.CharField(label='netIDs (Comma Separated)', max_length = 4000, 
		widget=forms.Textarea(attrs={'placeholder': 'netID1, netID2, etc.','style': 'width:400px; height:100px; font-size: 15px'}),required = True)
	year = forms.IntegerField(label="Members' year", required = True, initial=2016)

class row(forms.Form):
	check = forms.BooleanField(label="", required=False)

# class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
#         def confirm_login_allowed(self, user):
#             pass
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class AuthenticationForm(forms.Form):
    id_username = forms.CharField(label='Club name', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Club Name'}))
    id_password = forms.CharField(label='Club password', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Club Password'}))

class ExchangeForm(forms.Form):
    host_name = forms.CharField(label='Host netid', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Host NetID'}))
    guest_name = forms.CharField(label='Guest netid', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Guest NetID'}))

class GuestForm(forms.Form):
    host_name = forms.CharField(label='Host netid', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Host NetID'}))

class ClubPrefsForm(forms.Form):
	# timefields = [("6:00","6:00"), ("6:30","6:30"), ("7:00","7:00"), ("7:30", "7:30"), ("8:00","8:00"), ("8:30":"8:30"), ("9:00", "9:00"), ("9:30", "9:30"), ("10:00","10:00"), ("10:30","10:30"), ("11:00","11:00"), ("11:30", "11:30"), ("12:00","12:00"), ("12:30":"12:30"), ("13:00", "13:00"), ("13:30", "13:30"), ("14:00","14:00"), ("14:30","14:30"), ("15:00","15:00"), ("15:30", "15:30"), ("16:00","16:00"), ("16:30":"16:30"), ("17:00", "17:00"), ("17:30", "17:30"), ("18:00","18:00"), ("18:30","18:30"), ("19:00","19:00"), ("19:30", "19:30"), ("20:00","20:00"), ("20:30":"20:30"), ("21:00", "21:00"), ("21:30", "21:30")]

	timefields = [(" "," "), ("6:00","6:00"), ("6:30","6:30"), ("7:00","7:00"), ("7:30", "7:30"), ("8:00","8:00"), ("8:30", "8:30"), ("9:00", "9:00"), ("9:30", "9:30"), ("10:00","10:00"), ("10:30","10:30"), ("11:00","11:00"), ("11:30", "11:30"), ("12:00","12:00"), ("12:30", "12:30"), ("13:00", "13:00"), ("13:30", "13:30"), ("14:00","14:00"), ("14:30","14:30"), ("15:00","15:00"), ("15:30", "15:30"), ("16:00","16:00"), ("16:30", "16:30"), ("17:00", "17:00"), ("17:30", "17:30"), ("18:00","18:00"), ("18:30","18:30"), ("19:00","19:00"), ("19:30", "19:30"), ("20:00","20:00"), ("20:30", "20:30"), ("21:00", "21:00"), ("21:30", "21:30")]
	#club_name = forms.CharField(label='club name', max_length=100, required=False)

	b_start = forms.ChoiceField(timefields, label='Breakfast start time', required=True)
	b_end = forms.ChoiceField(timefields, label='Breakfast end time', required=True)
	l_start = forms.ChoiceField(timefields, label='Lunch start time', required=True)
	l_end = forms.ChoiceField(timefields, label='Lunch end time', required=True)
	d_start = forms.ChoiceField(timefields, label='Dinner start time', required=True)
	d_end = forms.ChoiceField(timefields, label='Dinner end time', required=True)
	br_start = forms.ChoiceField(timefields, label='Brunch start time', required=True)
	br_end = forms.ChoiceField(timefields, label='Brunch end time', required=True)

	# timefields = (("6:00","6:00"), ("6:30","6:30"), ("7:00","7:00"), ("7:30", "7:30"), ("8:00","8:00"), ("8:30":"8:30"),)
	# b_start = forms.TimeField(label='Breakfast start time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# b_end = forms.TimeField(label='Breakfast end time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# l_start = forms.TimeField(label='Lunch start time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# l_end = forms.TimeField(label='Lucnh end time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# d_start = forms.TimeField(label='Dinner start time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# d_end = forms.TimeField(label='Dinner end time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# br_start = forms.TimeField(label='Brunch start time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# br_end = forms.TimeField(label='Brunch end time', widget = forms.TimeInput(format='%H:%M'), required=False)

	max_guests = forms.IntegerField(label="Maximum number of guests", required = True, widget=forms.NumberInput(attrs={'style': 'width:62px; height:25px;'}))

class ViewExchangesForm(forms.Form):
	# ll = forms.BooleanField(label='Member netid', required=False)
    netid = forms.CharField(label='Member netid', max_length = 20, required=False)

class EditMembershipForm(forms.Form):
	netid = forms.CharField(label='Member netid', max_length = 20, required=True, initial="NetID")
	name = 	forms.CharField(label='Member name', max_length = 20, required=True, initial="Name")
	year = forms.IntegerField(label="Member year", required = True, initial=2016)

class AddMembersForm(forms.Form):
	names = forms.CharField(label='Names (Comma Separated)', max_length = 4000, required = True, initial="name1,name2")
	netIDs = forms.CharField(label='netIDs (Comma Separated)', max_length = 4000, required = True, initial="netID1,netID2")
	year = forms.IntegerField(label="Members' year", required = True, initial=2016)

class row(forms.Form):
	check = forms.BooleanField(label="", required=False)

# class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
#         def confirm_login_allowed(self, user):
#             pass
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

	timefields = [("6:00","6:00"), ("6:30","6:30"), ("7:00","7:00"), ("7:30", "7:30"), ("8:00","8:00"), ("8:30", "8:30"), ("9:00", "9:00"), ("9:30", "9:30"), ("10:00","10:00"), ("10:30","10:30"), ("11:00","11:00"), ("11:30", "11:30"), ("12:00","12:00"), ("12:30", "12:30"), ("13:00", "13:00"), ("13:30", "13:30"), ("14:00","14:00"), ("14:30","14:30"), ("15:00","15:00"), ("15:30", "15:30"), ("16:00","16:00"), ("16:30", "16:30"), ("17:00", "17:00"), ("17:30", "17:30"), ("18:00","18:00"), ("18:30","18:30"), ("19:00","19:00"), ("19:30", "19:30"), ("20:00","20:00"), ("20:30", "20:30"), ("21:00", "21:00"), ("21:30", "21:30")]
	club_name = forms.CharField(label='club name', max_length=100, required=False)

	b_start = forms.ChoiceField(timefields, label='Breakfast start time', required=False)
	b_end = forms.ChoiceField(timefields, label='Breakfast end time', required=False)
	l_start = forms.ChoiceField(timefields, label='Lunch start time', required=False)
	l_end = forms.ChoiceField(timefields, label='Lunch end time', required=False)
	d_start = forms.ChoiceField(timefields, label='Dinner start time', required=False)
	d_end = forms.ChoiceField(timefields, label='Dinner end time', required=False)
	br_start = forms.ChoiceField(timefields, label='Brunch start time', required=False)
	br_end = forms.ChoiceField(timefields, label='Brunch end time', required=False)

	# timefields = (("6:00","6:00"), ("6:30","6:30"), ("7:00","7:00"), ("7:30", "7:30"), ("8:00","8:00"), ("8:30":"8:30"),)
	# b_start = forms.TimeField(label='Breakfast start time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# b_end = forms.TimeField(label='Breakfast end time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# l_start = forms.TimeField(label='Lunch start time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# l_end = forms.TimeField(label='Lucnh end time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# d_start = forms.TimeField(label='Dinner start time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# d_end = forms.TimeField(label='Dinner end time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# br_start = forms.TimeField(label='Brunch start time', widget = forms.TimeInput(format='%H:%M'), required=False)
	# br_end = forms.TimeField(label='Brunch end time', widget = forms.TimeInput(format='%H:%M'), required=False)

	max_guests = forms.IntegerField(label="Maximum number of guest", required = False)

class ViewExchangesForm(forms.Form):
	# ll = forms.BooleanField(label='Member netid', required=False)
    netid = forms.CharField(label='Member netid', max_length=20, required=False)

class EditMembershipForm(forms.Form):
	name = 	forms.CharField(label='name', max_length=300, required=False)
	netid = forms.CharField(label='netid', max_length=20, required=False)
	year = forms.CharField(label='year', max_length=10, required=False)

class row(forms.Form):
	check = forms.BooleanField(label="", required=False)

# class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
#         def confirm_login_allowed(self, user):
#             pass
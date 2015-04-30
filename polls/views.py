from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import urllib, re
from polls.models import Exchanges, Members, ClubPrefs
import _ssl;_ssl.PROTOCOL_SSLv23 = _ssl.PROTOCOL_SSLv3
import os
import webbrowser
from time import sleep
from django.contrib.sessions.models import Session
from .forms import ExchangeForm, ClubPrefsForm, ViewExchangesForm, EditMembershipForm, GuestForm
from django import forms
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.requests import RequestSite
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone

@login_required(redirect_field_name = None)
def LogIn(request):

    # return HttpResponse("this is the club log in page")
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            f = form.cleaned_data
            if form.confirm_login_allowed(f['id_username']):
                return HttpResponseRedirect("Home/")

            user = authenticate(username=f['id_username'], password=f['id_password'])
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    # HttpResponse("User is valid, active and authenticated")
                    return HttpResponseRedirect("Home/")
                else:
                    return HttpResponse("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            return render(request, 'error.html')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

#@login_required(login_url = '/account/login/')
@login_required(redirect_field_name = None)
def Home(request):
    return render(request, 'home.html')

@login_required(redirect_field_name = None)
def Exchange(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ExchangeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            global host 
            host = form.cleaned_data['host_name']
            global guest 
            guest = form.cleaned_data['guest_name']

            try:
                guestObject = Members.objects.get(netID=str(guest))
            except:
                return render(request, 'errorExchange.html')
            try:
                hostObject = Members.objects.get(netID=str(host))
            except:
                return render(request, 'errorExchange.html')

            if (str(request.user) != hostObject.club):
                return render(request, 'error.html')

            meal = whichMeal(request, datetime.now())

            #a = Exchanges(hostName = host, guestName = guest, hostClub = str(request.user), guestClub = guestObject.club, month = datetime.now())
            #a.save()

            # increment host, decrement guest
            # person that's first in alphabetical order is always the "host"
            name1 = min(host, guest)
            name2 = max(host, guest)

            name1Club = Members.objects.get(netID=str(name1)).club
            name2Club = Members.objects.get(netID=str(name2)).club

            if (name1Club == name2Club):
                return render(request, 'error.html')

            # if exchange exists, get it
            try:
                exchangeObject = Exchanges.objects.get(hostName=str(name1), guestName=str(name2))

            # otherwise, new exchange
            except:
                exchangeObject = Exchanges(hostName = name1, guestName = name2, hostClub = name1Club, guestClub = name2Club, month = datetime.now())
                exchangeObject.save()


            print("which meal is it?" + meal)


            # if name1 is hosting, we increment
            if (host == name1):
                if (meal == "breakfast"):
                    exchangeObject.breakfast += 1
                    exchangeObject.save()
                elif (meal == "brunch"):
                    exchangeObject.brunch += 1
                    exchangeObject.save()
                elif (meal == "lunch"):
                    exchangeObject.lunch += 1
                    exchangeObject.save()
                elif (meal == "dinner"):
                    exchangeObject.dinner += 1
                    exchangeObject.save()

            #if name2 is hosting, we decrement
            if (host == name2):
                if (meal == "breakfast"):
                    exchangeObject.breakfast -= 1
                    exchangeObject.save()
                elif (meal == "brunch"):
                    exchangeObject.brunch -= 1
                    exchangeObject.save()
                elif (meal == "lunch"):
                    exchangeObject.lunch -= 1
                    exchangeObject.save()
                elif (meal == "dinner"):
                    exchangeObject.dinner -= 1
                    exchangeObject.save()


            # SEND CONFIRMATION EMAIL, netid@princeton.edu
            # first check that they are valid netids, if not, go to error page

            print "Thanks\n"
            print ("which club is using this right now? " + str(request.user))
            return HttpResponseRedirect("../Thanks/")
        else:
            print("form isnt valid \n")
            return render(request, 'errorExchange.html')
    else:
        form = ExchangeForm()

    return render(request, 'exchange.html', {'form': form})

@login_required(redirect_field_name = None)
def whichMeal(request, time):
    try:
        prefs = ClubPrefs.objects.get(club_name=str(request.user))
    except:
        return "no matching club"

    day = time.weekday()

    # if weekend 
    if (day > 5):
        if (prefs.br_start <= time <= prefs.br_end):
            meal = "brunch"
        if (prefs.d_start <= time <= prefs.d_end):
            meal = "dinner"

    else:
        if (prefs.b_start <= time <= prefs.b_end):
            meal = "breakfast"
        if (prefs.l_start <= time <= prefs.l_end):
            meal = "lunch"
        if (prefs.d_start <= time <= prefs.d_end):
            meal = "dinner"
    return meal




@login_required(redirect_field_name = None)
def Guest(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GuestForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            global host 
            host = form.cleaned_data['host_name']

            return HttpResponseRedirect("../Thanks/")
        else:
            return render(request, 'errorGuest.html')
    else:
        form = GuestForm()

    return render(request, 'guest.html', {'form': form})

@login_required(redirect_field_name = None)
def Thanks(request):
    return render(request, 'thanks.html')

def LoggedOut(request):
    return render(request, 'loggedout.html')

@login_required(redirect_field_name = None)
def Error(request):
    return render(request, 'error.html')

@login_required(redirect_field_name = None)
def SavedChanges(request):
    return render(request, 'savedchanges.html')

@login_required(redirect_field_name = None)
def ViewExchanges(request):
    exchanges = Exchanges.objects.all()       
    if request.method == 'POST': 
        form = ViewExchangesForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            print f
            # return SearchExchanges(request, f['netid'])
            exchanges = Exchanges.objects.filter(name1=f['netid'])
            return render(request, 'ViewExchanges.html',  {'form': form, 'exchanges' : exchanges})
        else:
            return render(request, 'errorViewExchanges.html')
    else:
        print "form isn't valid"
        form = ViewExchangesForm()

    return render(request, 'ViewExchanges.html', {'form': form, 'exchanges' : exchanges})    

@login_required(redirect_field_name = None)
def handleClubPrefs(request):
    if request.method == 'POST':
        form = ClubPrefsForm(request.POST)
        print "in post"
        if form.is_valid():
            f = form.cleaned_data
            print f

            previousEntries = ClubPrefs.objects.filter(club_name=str(request.user)).delete()

            c = ClubPrefs(b_start=f['b_start'], l_start=f['l_start'], d_start=f['d_start'], br_start=f['br_start'],
            b_end=f['b_end'], l_end=f['l_end'], d_end=f['d_end'], br_end=f['br_end'], max_guests=f['max_guests'], club_name=str(request.user))
            
            c.save()
            print ClubPrefs.objects.all()
            return HttpResponseRedirect("../SavedChanges")
        else:
            return render(request, 'errorClubPreferences.html')
    else:
        form = ClubPrefsForm()

    return render(request, 'clubprefs.html', {'form': form})

@login_required(redirect_field_name = None)
def EditMembership(request):
    membership = Members.objects.all()       
    if request.method == 'POST':
        form = EditMembershipForm(request.POST)

        if form.is_valid():
            f = form.cleaned_data
            print f
            return HttpResponse("Here's your membership.")
        else:
            return render(request, 'errorEditMembership.html')
    else:
        form = EditMembershipForm()

    return render(request, 'EditMembership.html', {'form': form}) 

def Confirmation(request, anystring=None):
    if (anystring):
        print("we got an anystring varable: " + anystring)




# --------------------------------------------

# def HostLogIn(request):
#     global freshRequest
#     freshRequest = request
#     hostRequest = request
#     print "host page: " + str(request)
#     print request.POST 
#     return check_login(request, "http://localhost:8000/Xchange/VisitorLogIn", "host")

    #print "<p>Think of this as the main page of your application after %s has been authenticated." % (netid)


# def VisitorLogIn(request):
    #return HttpResponse("Hello, world. You're at the vISITOR lOGin.")
    # print "visitor page: " + str(request)
    # return check_login(freshRequest, "http://localhost:8000/Xchange", "guest")
    # return check_login(request, "http://localhost:8000/Xchange", "guest")

# def LogOut(request):
#     request.session['netid'] = None
    #request.session.flush()
    # return HttpResponseRedirect("http://fed.princeton.edu/cas/logout")


# def check_login(request, redirect, person):
#     print "request is = " + str(request)
#     cas_url = "https://fed.princeton.edu/cas/"
#     service_url = 'http://' + urllib.quote(request.META['HTTP_HOST'] + request.META['PATH_INFO'])
#     service_url = re.sub(r'ticket=[^&]*&?', '', service_url)
#     service_url = re.sub(r'\?&?$|&$', '', service_url)
#     if "ticket" in request.GET:
#         val_url = cas_url + "validate?service=" + service_url + '&ticket=' + urllib.quote(request.GET['ticket'])
#         r = urllib.urlopen(val_url).readlines() #returns 2 lines
        
#         print "r = " + str(r)
#         print "val_url = " + str(val_url)

#         if len(r) == 2 and re.match("yes", r[0]) != None:

#             request.session['netid'] = r[1].strip()

#             if(str(person) == "host"):
#                 hostNetId = request.session['netid']
#             elif(str(person) == "guest"):
#                 guestNetId = request.session['netid']

#             # LogOut(request)
#             sleep(1)
#             webbrowser.open("https://fed.princeton.edu/cas/logout")
#             sleep(1)
#             # print "Are we in a loop?"
#             return HttpResponseRedirect(redirect)
#         else:
#             return HttpResponse("FAILURE")
#     else:
#         login_url = cas_url + 'login?service=' + service_url
#         return HttpResponseRedirect(login_url)
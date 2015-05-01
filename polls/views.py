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
from .tables import SimpleTable, NameTable
from django_tables2   import RequestConfig

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
                print "guest is"
                guestObject = Members.objects.get(netID=str(guest))
            except:
                print "Guest Object not found"
                return render(request, 'errorExchange.html')
            try:
                print "host is"
                hostObject = Members.objects.get(netID=str(host))
            except:
                print "Host Object not found"
                return render(request, 'errorExchange.html')

            if (str(request.user) != hostObject.club):
                print "%s != %s"%(str(request.user), str(hostObject.club))
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
def whichMeal(request, date_time):
    time = date_time.time()
    try:
        prefs = ClubPrefs.objects.get(club_name=str(request.user))
    except:
        print "no club"
        return "no matching club"

    day = date_time.weekday()
    print "day is " + str(day)
    meal = "null"
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
    print "in edit membership"
    membership = Members.objects.filter(club=str(request.user)) 
    members = []
    for member in membership:

        m = {}
        m["netID"] = member.netID
        m["name"] = member.name
        m["year"] = member.year
        members.append(m)

    print members
    if request.method == "POST":
        print request
        print "its a post method"
        # table = SimpleTable(members)
        # RequestConfig(request).configure(table)
        
        selected = request.POST.getlist("Amend")
        select_objects = Members.objects.filter(netID__in=selected)
        print "SELECTED OBJECTS"
        print select_objects
        return HttpResponse("It worked")
    else:
        print request
        print "we'rre in the esle"
        table = SimpleTable(members)
        RequestConfig(request).configure(table)


    return render(request, 'EditMembership2.html', {'table': table})


    # return render(request, 'people.html', {'table': table})
    # if request.method == 'POST':
    #     form = EditMembershipForm(request.POST, members=membership)

    #     if form.is_valid():
    #         f = form.cleaned_data
    #         print f
    #         return HttpResponse("Here's your membership.")
    #     else:
    #         return render(request, 'errorEditMembership.html')
    # else:
    #     form = EditMembershipForm(members=membership)

    # return render(request, 'EditMembership.html', {'form': form, 'members': membership}) 

def Confirmation(request, anystring=None):
    if (anystring):
        print("we got an anystring varable: " + anystring)

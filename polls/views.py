from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import urllib, re
from polls.models import Exchanges, Members, ClubPrefs, ConfirmExchange
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
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
import random, string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def id_generator(size):
    l = ["filler"]
    s = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for i in xrange(size))
    # while len(l) == 0:
    #     s = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for i in xrange(size))
    #     l = ConfirmExchange.objects.filter(Q(hostConfirm=s) | Q(guestConfirm=s))
    print s
    return s

def send_email_plz(link, netid):
    subject = 'Confirm Meal Exchange'
    email = netid + "@princeton.edu"
    to = [email]
    from_email = settings.DEFAULT_FROM_EMAIL

    ctx = {
    'user': netid,
    'link': link
    }

    message_text = render_to_string('confirm3.txt', ctx)

    EmailMessage(subject, message_text, to=to, from_email=from_email).send()

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

            if (hostObject.club == guestObject.club):
                return render(request, 'error.html')
            #a = Exchanges(hostName = host, guestName = guest, hostClub = str(request.user), guestClub = guestObject.club, month = datetime.now())
            #a.save()

            # increment host, decrement guest
            # person that's first in alphabetical order is always the "host"
            name1 = host
            name2 = guest

            print "confirming "
            exchange_str = "%s, %s, %s"%(name1, name2, meal)
            host_id = id_generator(64)
            guest_id = id_generator(64)
            confirm = ConfirmExchange(hostConfirmString=host_id, guestConfirmString=guest_id, exchange_str=exchange_str, hostHasConfirmed=False, guestHasConfirmed=False)
            confirm.save()

            print confirm

            host_signup_link = "localhost:8000/Xchange/Confirmation/" + confirm.hostConfirmString
            guest_signup_link = "localhost:8000/Xchange/Confirmation/" + confirm.guestConfirmString


            print "host signup link: " + host_signup_link
            print "host: " + host
            send_email_plz(host_signup_link, host)

            print "should have just sent to host"
            send_email_plz(guest_signup_link, guest)
            print "should have just sent to guest"

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
    exchanges = Exchanges.objects.filter(hostClub=request.user)
    # exchanges2 =  Exchanges.objects.filter(guestClub=request.user)
    print "exchanges"
    print exchanges
    # print "exchanges2"
    # print exchanges2
    if request.method == 'POST': 
        form = ViewExchangesForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            print f
            # return SearchExchanges(request, f['netid'])
            exchanges = Exchanges.objects.filter( Q(hostClub=request.user) & Q(hostName=f['netid']) )
            # return render(request, 'ViewExchanges.html',  {'form': form, 'exchanges' : exchanges})
            return render(request, 'ViewExchanges2.html', {'form': form, 'exchanges' : exchanges})
        else:
            print "invalid form"
            return render(request, 'errorViewExchanges.html')
    else:
        print "form empty"
        form = ViewExchangesForm()

    return render(request, 'ViewExchanges2.html', {'form': form, 'exchanges' : exchanges})
    # return render(request, 'ViewExchanges2.html', {'form': form, 'exchanges' : exchanges})    

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
        table = SimpleTable(members)
        RequestConfig(request).configure(table)


    #return render(request, 'EditMembership2.html', {'table': table})
    return render(request, 'ViewMembership.html', {'table': table})

def Confirmation(request, anystring=None):
    print "Confirmation"
    if (anystring):
        print("we got an anystring varable: " + anystring)

        hc = ConfirmExchange.objects.filter(hostConfirmString=anystring)
        gc = ConfirmExchange.objects.filter(guestConfirmString=anystring)

        if (len(hc) > 0):
            hc[0].hostHasConfirmed = True
            hc[0].save()
            c = hc[0]
        if (len(gc) > 0):
            gc[0].guestHasConfirmed = True
            gc[0].save()
            c = gc[0]

        if c.guestHasConfirmed and c.hostHasConfirmed:
            print "both confirmed"
            exchange_obj_str = re.split("\s*,\s*", c.exchange_str)
            print exchange_obj_str

            name1 = exchange_obj_str[0]
            name2 = exchange_obj_str[1]
            meal = exchange_obj_str[2]
            name1Club = Members.objects.get(netID=str(exchange_obj_str[0])).club
            name2Club = Members.objects.get(netID=str(exchange_obj_str[1])).club
            # if exchange exists, get it
            try:
                print "this exchange object exists"
                exchangeHostObject = Exchanges.objects.get(hostName=str(name1), guestName=str(name2))
                exchangeGuestObject = Exchanges.objects.get(guestName=str(name1), hostName=str(name2))
                print "exchange Host - "
                print exchangeHostObject
                print "exchange Guest - "
                print exchangeGuestObject
            # otherwise, new exchange
            except:
                exchangeHostObject = Exchanges(hostName = name1, guestName = name2, hostClub = name1Club, guestClub = name2Club, month = datetime.now())
                exchangeHostObject.save()
                exchangeGuestObject = Exchanges(guestName = name1, hostName = name2, guestClub = name1Club, hostClub = name2Club, month = datetime.now())
                exchangeGuestObject.save()


            print("which meal is it?" + meal)
        # if name1 is hosting, we increment
            if (meal == "breakfast"):
                exchangeHostObject.breakfast += 1
                exchangeGuestObject.breakfast -= 1
                exchangeHostObject.save()
                exchangeGuestObject.save()
            elif (meal == "brunch"):
                exchangeHostObject.brunch += 1
                exchangeGuestObject.brunch -= 1
                exchangeHostObject.save()
                exchangeGuestObject.save()
            elif (meal == "lunch"):
                print "its lunch"
                exchangeHostObject.lunch += 1
                exchangeGuestObject.lunch -= 1
                exchangeHostObject.save()
                exchangeGuestObject.save()
            elif (meal == "dinner"):
                exchangeHostObject.dinner += 1
                exchangeGuestObject.dinner -= 1
                exchangeHostObject.save()
                exchangeGuestObject.save()

            c.delete()
        return HttpResponse("Great.")
    return HttpResponse("that's not valid")
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
from .forms import ExchangeForm, ClubPrefsForm, ViewExchangesForm, AddMembersForm, EditMembershipForm, GuestForm
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
import xlwt



def createCSV(clubName):
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
        num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    wb = xlwt.Workbook()

    # create sheets
    memList = wb.add_sheet('MemberList')
    exchanges = wb.add_sheet('Exchanges')

    # get member list for a club
    memberList = Members.objects.filter(club=clubName)
    memberList = memberList.extra(order_by=['name'])

    # get all exchanges where a member of this club is a host
    exchangeList = Exchanges.objects.filter(hostClub = clubName)
    exchangeList = exchangeList.extra(order_by=['hostName'])

    added_exchanges = {}
    for e in exchangeList:
        # if not in dictionary already, add it
        if e.hostName not in added_exchanges:
            member = Members.objects.get(netID=e.hostName)
            added_exchanges[e.hostName] = [member.name, e.breakfast, e.brunch, e.lunch, e.dinner]

        # if already in, we add to the values 
        else:
            old_values = added_exchanges[e.hostName]
            added_exchanges[e.hostName] = [old_values[0], old_values[1] + e.breakfast, old_values[2] + e.brunch, old_values[3] + e.lunch, old_values[4] + e.dinner]


    # sort the added_exchanges by name
    sorted_exchanges = sorted(added_exchanges.items(), key=lambda e: e[1][0])



    # now we can write to the excel file


    # member list
    memList.write(0, 0, "Members")
    for i in range(0, len(memberList)):
        memList.write(i+1, 0, memberList[i].name)
        memList.write(i+1, 1, memberList[i].netID)
        memList.write(i+1, 2, memberList[i].year)

    # exchange list
    exchanges.write(0, 0, "Member Name")
    exchanges.write(0, 1, "netID")
    exchanges.write(0, 2, "Outstanding Breakfasts")
    exchanges.write(0, 3, "Outstanding Brunches")
    exchanges.write(0, 4, "Outstanding Lunches")
    exchanges.write(0, 5, "Outstanding Dinners")

    print sorted_exchanges

    for i in range(0, len(sorted_exchanges)):
        exchanges.write(i+1, 0, str(sorted_exchanges[i][1][0]))
        exchanges.write(i+1, 1, str(sorted_exchanges[i][0]))
        exchanges.write(i+1, 2, str(sorted_exchanges[i][1][1]))
        exchanges.write(i+1, 3, str(sorted_exchanges[i][1][2]))
        exchanges.write(i+1, 4, str(sorted_exchanges[i][1][3]))
        exchanges.write(i+1, 5, str(sorted_exchanges[i][1][4]))

    wb.save('example2.xls')
    return wb


def id_generator(size):
    l = ["filler"]
    s = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for i in xrange(size))
    # while len(l) == 0:
    #     s = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for i in xrange(size))
    #     l = ConfirmExchange.objects.filter(Q(hostConfirm=s) | Q(guestConfirm=s))
    print s
    return s

def calculateOutstanding(netid):

    exchanges = Exchanges.objects.filter(hostName=netid)
    member = Members.objects.get(netID=netid)

    hostBreakfast = 0
    hostBrunch = 0
    hostLunch = 0
    hostDinner = 0
    guestBreakfast = 0
    guestBrunch = 0
    guestLunch = 0
    guestDinner = 0
    youUnconfirmed = 0
    otherUnconfirmed = 0

    # confirmed exchanges
    for exchange in exchanges:


        if exchange.breakfast < 0:
            guestBreakfast += abs(exchange.breakfast)
        else:
            hostBreakfast += abs(exchange.breakfast)

        if exchange.brunch < 0:
            guestBrunch += abs(exchange.brunch)
        else:
            hostBrunch += abs(exchange.brunch)

        if exchange.lunch < 0:
            guestLunch += abs(exchange.lunch)
        else:
            hostLunch += abs(exchange.lunch)

        if exchange.dinner < 0:
            guestDinner += abs(exchange.dinner)
        else:
            hostDinner += abs(exchange.dinner)


    # unconfirmed exchanges
    unconfirmed = ConfirmExchange.objects.filter(host=netid)
    for confirmExchange in unconfirmed:
        if confirmExchange.hostHasConfirmed:
            otherUnconfirmed += 1
        else:
            youUnconfirmed += 1

    outstanding = {
    'hostBreakfast': hostBreakfast,
    'hostBrunch': hostBrunch,
    'hostLunch': hostLunch,
    'hostDinner': hostDinner,
    'guestBreakfast': guestBreakfast,
    'guestBrunch': guestBrunch,
    'guestLunch': guestLunch,
    'guestDinner': guestDinner,
    'guest': member.numguests,
    'youUnconfirmed': youUnconfirmed,
    'otherUnconfirmed': otherUnconfirmed
    }

    print "outstanding"
    print outstanding
    return outstanding

def send_email_plz(link, netid):
    subject = 'Confirm Meal Exchange'
    email = netid + "@princeton.edu"
    to = [email]
    from_email = settings.DEFAULT_FROM_EMAIL

    outstanding = calculateOutstanding(netid)

    ctx = {
    'user': netid,
    'link': link,
    'hostBreakfast': outstanding['hostBreakfast'],
    'hostBrunch': outstanding['hostBrunch'],
    'hostLunch': outstanding['hostLunch'],
    'hostDinner': outstanding['hostDinner'],
    'guestBreakfast': outstanding['guestBreakfast'],
    'guestBrunch': outstanding['guestBrunch'],
    'guestLunch': outstanding['guestLunch'],
    'guestDinner': outstanding['guestDinner'],
    'guest': outstanding['guest'],
    'youUnconfirmed': outstanding['youUnconfirmed'],
    'otherUnconfirmed': outstanding['otherUnconfirmed']
    }

    message_text = render_to_string('confirm3.txt', ctx)

    EmailMessage(subject, message_text, to=to, from_email=from_email).send()

@login_required(redirect_field_name = None)
def SendEmails(request):
    # send emails to anyone who has not fulfilled both sides of a meal exchange

    members = Members.objects.filter(club=request.user)
    for member in members:

        outstanding = calculateOutstanding(member.netID)

        subject = 'Meal Exchange Reminder'
        to = member.netID + "@princeton.edu"

        ctx = {
            'user': netid,
            'hostBreakfast': outstanding['hostBreakfast'],
            'hostBrunch': outstanding['hostBrunch'],
            'hostLunch': outstanding['hostLunch'],
            'hostDinner': outstanding['hostDinner'],
            'guestBreakfast': outstanding['guestBreakfast'],
            'guestBrunch': outstanding['guestBrunch'],
            'guestLunch': outstanding['guestLunch'],
            'guestDinner': outstanding['guestDinner']
            }

        message_text = render_to_string('endOfMonth.txt', ctx)
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
            return render(request, 'error.html', {'message': "Login failed"})
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

#@login_required(login_url = '/account/login/')
@login_required(redirect_field_name = None)
def Home(request):

    # check month, if the month is new, we reset everyone's guest meals
    try:
        clubPrefs = ClubPrefs.objects.get(club_name=request.user)
    except:
        return HttpResponseRedirect('../ClubPrefs')

    if (datetime.today().month != clubPrefs.last_login):
        # reset everyone's guest meals
        members = Members.objects.filter(club=request.user)
        for member in members:
            member.numguests = clubPrefs.max_guests
            member.save()

        clubPrefs.last_login = datetime.today().month
        clubPrefs.save()

    return render(request, 'home.html')


@login_required(redirect_field_name = None)
def DownloadLink(request):
    clubName = request.user

    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
        num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    wb = xlwt.Workbook()

    # create sheets
    memList = wb.add_sheet('MemberList')
    exchanges = wb.add_sheet('Exchanges')

    # get member list for a club
    memberList = Members.objects.filter(club=clubName)
    memberList = memberList.extra(order_by=['name'])

    # get all exchanges where a member of this club is a host
    exchangeList = Exchanges.objects.filter(hostClub = clubName)
    exchangeList = exchangeList.extra(order_by=['hostName'])

    added_exchanges = {}
    for e in exchangeList:
        # if not in dictionary already, add it
        if e.hostName not in added_exchanges:
            member = Members.objects.get(netID=e.hostName)
            added_exchanges[e.hostName] = [member.name, e.breakfast, e.brunch, e.lunch, e.dinner]

        # if already in, we add to the values 
        else:
            old_values = added_exchanges[e.hostName]
            added_exchanges[e.hostName] = [old_values[0], old_values[1] + e.breakfast, old_values[2] + e.brunch, old_values[3] + e.lunch, old_values[4] + e.dinner]


    # sort the added_exchanges by name
    sorted_exchanges = sorted(added_exchanges.items(), key=lambda e: e[1][0])



    # now we can write to the excel file


    # member list
    memList.write(0, 0, "Members")
    for i in range(0, len(memberList)):
        memList.write(i+1, 0, memberList[i].name)
        memList.write(i+1, 1, memberList[i].netID)
        memList.write(i+1, 2, memberList[i].year)

    # exchange list
    exchanges.write(0, 0, "Member Name")
    exchanges.write(0, 1, "netID")
    exchanges.write(0, 2, "Outstanding Breakfasts")
    exchanges.write(0, 3, "Outstanding Brunches")
    exchanges.write(0, 4, "Outstanding Lunches")
    exchanges.write(0, 5, "Outstanding Dinners")

    print sorted_exchanges

    for i in range(0, len(sorted_exchanges)):
        exchanges.write(i+1, 0, str(sorted_exchanges[i][1][0]))
        exchanges.write(i+1, 1, str(sorted_exchanges[i][0]))
        exchanges.write(i+1, 2, str(sorted_exchanges[i][1][1]))
        exchanges.write(i+1, 3, str(sorted_exchanges[i][1][2]))
        exchanges.write(i+1, 4, str(sorted_exchanges[i][1][3]))
        exchanges.write(i+1, 5, str(sorted_exchanges[i][1][4]))



    wb.save('example2.xls')
    f = open('example2.xls', 'rw')
    response = HttpResponse(f)
    response['Content-Disposition'] = 'attachment; filename="example2.xls"'
    return response

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
                return render(request, 'error.html', {'message': "Guest netid not found"})
            try:
                print "host is"
                hostObject = Members.objects.get(netID=str(host))
            except:
                print "Host Object not found"
                return render(request, 'error.html', {'message': "Host netid not found"})

            if (str(request.user) != hostObject.club):
                print "%s != %s"%(str(request.user), str(hostObject.club))
                return render(request, 'error.html', {'message': "Host is not a member of this club"})

            meal = whichMeal(request, datetime.now())

            if (hostObject.club == guestObject.club):
                return render(request, 'error.html', {'message': "Host and guest can't be from same club"})
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
            confirm = ConfirmExchange(hostConfirmString=host_id, guestConfirmString=guest_id, exchange_str=exchange_str, hostHasConfirmed=False, guestHasConfirmed=False, host = name1, guest = name2)
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

            # if host name not in host club, error
            try:
                member = Members.objects.get(netID=host)
            except:
                print ("couldnt find a member")
                return render(request, 'error.html', {'message': "Invalid host netID"})

            if (str(member.club) != str(request.user)):
                print("member club: " + str(member.club))
                print("request.user: " + str(request.user))
                return render(request, 'error.html', {'message': "Host not a member of this club"})

            # if they're out
            if (member.numguests < 1):
                return render(request, 'error.html', {'message': "You're out of guest meals! Lol go eat at a Dining Hall"})

            member.numguests -= 1
            member.save()

            return HttpResponseRedirect("../Thanks/")
        else:
            return render(request, 'error.html', {'message': "Error registering guest"})
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

            exchanges = exchanges.extra(order_by=['hostName'])
            # return render(request, 'ViewExchanges.html',  {'form': form, 'exchanges' : exchanges})
            return render(request, 'ViewExchanges2.html', {'form': form, 'exchanges' : exchanges})
        else:
            print "invalid form"
            return render(request, 'error.html', {'message': "Error loading the form"})
    else:
        print "form empty"
        form = ViewExchangesForm()

    return render(request, 'ViewExchanges2.html', {'form': form, 'exchanges' : exchanges})
    # return render(request, 'ViewExchanges2.html', {'form': form, 'exchanges' : exchanges})  

@login_required(redirect_field_name = None)
def handleClubPrefs(request):
    oldPrefs = ClubPrefs.objects.get(club_name=request.user)
    if request.method == 'POST':

        form = ClubPrefsForm(request.POST, oldPrefs=oldPrefs)
        print "in post"
        if form.is_valid():
            f = form.cleaned_data
            print f

            previousEntries = ClubPrefs.objects.filter(club_name=str(request.user)).delete()

            c = ClubPrefs(b_start=f['b_start'], l_start=f['l_start'], d_start=f['d_start'], br_start=f['br_start'],
            b_end=f['b_end'], l_end=f['l_end'], d_end=f['d_end'], br_end=f['br_end'], max_guests=f['max_guests'], club_name=str(request.user), last_login=datetime.today().month)
            
            c.save()
            print ClubPrefs.objects.all()
            return HttpResponseRedirect("../SavedChanges")
        else:
            return render(request, 'error.html', {'message': "You didn't fill out all the preferences!"})
    else:
        form = ClubPrefsForm(oldPrefs=oldPrefs)

    return render(request, 'clubprefs.html', {'form': form})

@login_required(redirect_field_name = None)
def EditMembership(request):
    print "in edit membership"

    membership = Members.objects.filter(club=str(request.user)) 

    membership = membership.extra(order_by=['name'])
    members = []

    for member in membership:

        m = {}
        m["netID"] = member.netID
        m["name"] = member.name
        m["year"] = member.year
        members.append(m)

    print members
    if request.method == "POST":
        print "IN ELSE STATMENT"

        selected = request.POST.getlist("Amend")
        select_objects = Members.objects.filter(netID__in=selected)
        print "SELECTED OBJECTS"
        print select_objects
        for item in select_objects:
            item.delete()
        return HttpResponseRedirect('../EditMembership')
    else:
        print "adding a prefix"
        print request
        table = SimpleTable(members)
        RequestConfig(request).configure(table)


    #return render(request, 'EditMembership2.html', {'table': table})
    return render(request, 'ViewMembership.html', {'table': table})

def AddMembers(request):
    try:
        clubPrefs = ClubPrefs.objects.get(club_name=request.user)
    except: 
        return HttpResponseRedirect('../ClubPrefs')

    max_guests = clubPrefs.max_guests
    club = request.user

    if request.method == 'POST':
        addMembers = AddMembersForm(request.POST)

        if addMembers.is_valid():
            f = addMembers.cleaned_data
            print f
            
            # do stuf
            f = addMembers.cleaned_data
            names = re.split('\s*,\s*', str(f['names']))
            # names = re.split(',', str(f['names']))
            # netIDs = re.split(',', str(f['netIDs']))

            netIDs = re.split('\s*,\s*', str(f['netIDs']))
            year = f['year']

            # for name in names:
            #     if re.match("\s*", name):
            #         print "removing name"
            #         names.remove(name)

            # for netID in netIDs:
            #     if re.match("\s*", netID):
            #         print "removing netID"
            #         netIDs.remove(netID)

            # have to have same amount of names and netIDS
            if len(names) != len(netIDs):
                return render(request, 'error.html', {'message': "Need same number of names and netIDs"})

            print "for loop for adding members"
            print "names: " + str(names)
            print "netids: " + str(netIDs)
            count = 0
            for netID in netIDs:
                m = Members(name=names[count], netID=netID, year=year, numguests=max_guests, club=club)
                print "saving a member"
                m.save()
                count += 1

            return HttpResponseRedirect("../EditMembership")
        else:
            return render(request, 'error.html', {'message': "Error adding members."})
    else:
        addMembers = AddMembersForm()

    return render(request, 'AddMembers.html', {'form': addMembers})

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
        return HttpResponseRedirect("../Thanks/")
    return render(request, 'error.html', {'message': "Error: meal exchange not confirmed"})
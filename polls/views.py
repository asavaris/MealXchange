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


class RemoveNextMiddleWare(object):
    def process_request(self, object):
        if request.path == settings.LOGIN_URL and request.Get.has_key('next'):
            return HttpResponseRedirect(settings.LOGIN_URL)


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
            return HttpResponse("The username and password were incorrect.")
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

            # Exchanges.objects.all()
            # a = Exchanges(name1 = guest, name2 = host, club1 = 'terrace', club2 = 'tower', month = datetime.now())
            # a.save()
            # print Exchanges.objects.all()

            print "Thanks"
            return HttpResponseRedirect("../Thanks/")
    else:
        # print "form isn't valid"
        form = ExchangeForm()

    return render(request, 'exchange.html', {'form': form})

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
        # print "form isn't valid"
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

# def ExchangeThanks(request):
#     return HttpResponse(host + " hosted " + guest)

# def GuestThanks(request):
#     return HttpResponse(host + " hosted a guest")

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
        print "form isn't valid"
        form = ViewExchangesForm()

    return render(request, 'ViewExchanges.html', {'form': form, 'exchanges' : exchanges})    

@login_required(redirect_field_name = None)
def ClubPrefs(request):
    if request.method == 'POST':
        form = ClubPrefsForm(request.POST)
        print "in post"
        if form.is_valid():
            f = form.cleaned_data
            print f

            c = ClubPrefs(b_start=f['b_start'], l_start=f['l_start'], d_start=f['d_start'], br_start=f['br_start'],
            b_end=f['b_end'], l_end=f['l_end'], d_end=f['d_end'], br_end=f['br_end'], max_guests=f['max_guests'])
            
            c.save()
            print ClubPrefs.objects.all()
            return HttpResponseRedirect("LogIn/")
    else:
        print "form isn't valid"
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
        form = EditMembershipForm()

    return render(request, 'EditMembership.html', {'form': form}) 

@login_required(redirect_field_name = None)
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

@login_required(redirect_field_name = None)
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

@login_required(redirect_field_name = None)
def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

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
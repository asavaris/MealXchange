@login_required(redirect_field_name = None)
def handleClubPrefs(request):
    if request.method == 'POST':
        # try:
        #     oldPrefs = ClubPrefs.objects.get(club_name=request.user)
        #     form = ClubPrefsForm(request.POST, initial={'b_start': oldPrefs.b_start, 'b_end': oldPrefs.b_end, 'br_start': oldPrefs.br_start, 'br_end': oldPrefs.br_end, 'l_start': oldPrefs.l_start, 'l_end': oldPrefs.l_end, 'd_start': oldPrefs.d_start, 'd_end': oldPrefs.d_end, 'max_guests': oldPrefs.max_guests}, label_suffix='')
        # except:
        #     print "Shouldnt get here"
        form = ClubPrefsForm(request.POST, label_suffix='')

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
        # try:
        #     print "in try else"
        #     oldPrefs = ClubPrefs.objects.get(club_name=request.user)
        #     print "does it get to the form"
        #     form = ClubPrefsForm(request, initial={'b_start': oldPrefs.b_start, 'b_end': oldPrefs.b_end, 'br_start': oldPrefs.br_start, 'br_end': oldPrefs.br_end, 'l_start': oldPrefs.l_start, 'l_end': oldPrefs.l_end, 'd_start': oldPrefs.d_start, 'd_end': oldPrefs.d_end, 'max_guests': oldPrefs.max_guests}, label_suffix='')
        # except:
        #     print "in excpet else"
        form = ClubPrefsForm(request, label_suffix='')

    #return render(request, 'clubprefs.html', {'form': form})
    return render(request, 'SimpleClubPrefs.html', {'form': form})

import xlwt
from datetime import datetime
from polls.models import Exchanges, Members, ClubPrefs, ConfirmExchange

# COLUMNS GO FIRST: two clubs, five members
# clubsMembers = [[0 for x in range(2)] for x in range(4)] 

# clubsMembers[0][0] = "Asavari Sinha"
# clubsMembers[1][0] = "Michael Buono"
# clubsMembers[0][1] = "Paco Avila"
# clubsMembers[1][1] = "Louis Guerra"
# clubsMembers[2][1] = "Ava Chen"

# clubs = ["Tower", "Terrace"]

def __init__(clubName):
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
	ws.write(0, 0, "Members")
	for i in range(0, len(memberList)):
		ws.write(i+1, 0, memberList[i].name)
		ws.write(i+1, 1, memberList[i].netID)
		ws.write(i+1, 2, memberList[i].year)



	# for i in range(0, len(clubs)):
	#     ws.write(0, i, clubs[i])

	# for i in range (0, len(clubsMembers)):
	#     for j in range(0, len(clubsMembers[0])):
	#         ws.write(i + 1, j, clubsMembers[i][j])

	#ws.write(0, 0, 1234.56, style0)
	#ws.write(1, 0, datetime.now(), style1)
	#ws.write(2, 0, 1)
	#ws.write(2, 1, 1)
	#ws.write(2, 2, xlwt.Formula("A3+B3"))

	wb.save('example2.xls')

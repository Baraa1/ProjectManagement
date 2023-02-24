# Python
from datetime import datetime
import calendar
import pytz
# Django
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
# Mine
from dockingRecords.models import *
from locations.models import Stand
from accounts.models import CustomUser
from dockingRecords.decorators import *


tz = pytz.timezone('Asia/Riyadh')

@login_required(login_url='login')
@user_passes_test(view_records)
def filter_month(request):
    year = datetime.now().year
    month = datetime.now().month
    # Return a matrix (list of lists) representing a month's calendar.
    # Each row represents a week; week entries are datetime.date values.
    month_calendar = calendar.Calendar()
    month_calendar.setfirstweekday(calendar.SUNDAY)
    month_calendar = calendar.Calendar().monthdatescalendar(year,month)
    weeks_dict = {}
    
    # user filtered chart
    if request.method == 'POST':
        new_date = request.POST.get('month')
        # slice html input type=month
        year = int(new_date[0:4])
        month = int(new_date[5:])
        month_calendar = calendar.Calendar().monthdatescalendar(year, month)

        # get the amounts of records created each week
        for week in month_calendar:
            row = int(month_calendar.index(week))
            weeks_dict[f'Week {row+1}'] = len(DockingRecord.objects.filter(Q(docked__gte = month_calendar[row][0]) & Q(docked__lte = month_calendar[row][6])))

        context = {
                "weeks_dict":weeks_dict,
                "filtered":'true',
            }
        
        return render(request, 'htmx/month-filtered.html', context=context)
    
    # default chart
    for week in month_calendar:
        row = int(month_calendar.index(week))
        weeks_dict[f'Week {row+1}'] = len(DockingRecord.objects.filter(Q(docked__gte = month_calendar[row][0]) & Q(docked__lte = month_calendar[row][6])))

    return weeks_dict, 'false'

@login_required(login_url='login')
@user_passes_test(view_records)
def filter_stands(request):
    stands = Stand.objects.all()
    stands_dict = {}
    
    # user filtered chart
    if request.method == 'POST':
        from_date = request.POST.get('from')
        to_date = request.POST.get('to')
        stand = request.POST.get('stand')
        # if stand specified
        if stand:
            print("if stand ")
            stand_name = Stand.objects.get(id = stand).stand_name
            if from_date:
                if to_date:
                    stands_dict[stand_name] = len(DockingRecord.objects.filter(Q(docked__gte = from_date) & Q(docked__lte = to_date) & Q(stand = stand)))
                else:
                    stands_dict[stand_name] = len(DockingRecord.objects.filter(Q(docked__gte = from_date) & Q(stand = stand)))
            else:
                stands_dict[stand_name] = len(DockingRecord.objects.filter(stand = stand))
        else:
            for stand in stands:
                if from_date:
                    if to_date:
                        stands_dict[stand.stand_name] = len(DockingRecord.objects.filter(Q(stand = stand) & Q(docked__gte = from_date) & Q(docked__lte = to_date)))
                    else:
                        stands_dict[stand.stand_name] = len(DockingRecord.objects.filter(Q(stand = stand) & Q(docked__gte = from_date)))
                elif to_date:
                    stands_dict[stand.stand_name] = len(DockingRecord.objects.filter(Q(stand = stand) & Q(docked__lte = to_date)))
            print(stands_dict)
        
        context = {
            "stands": stands,
            "stands_dict": stands_dict,
        }
        return render(request, 'htmx/stands-filtered.html', context=context)

    # default chart
    for stand in stands:
        stands_dict[stand.stand_name] = len(DockingRecord.objects.filter(stand = stand))

    return stands, stands_dict

@login_required(login_url='login')
@user_passes_test(view_records)
def filter_users(request):
    users = CustomUser.objects.filter(is_superuser = False, groups__name='Operator')
    users_dict = {}

    if request.method == 'POST':
        from_date = request.POST.get('users-from')
        to_date = request.POST.get('users-to')

        for user in users:
            user2 = SecondOperator.objects.get(second_operator = user)

            if from_date:
                if to_date:# get the records where the date is after from date and before to date and operator1 or operator2 = user 
                    users_dict[f'{user.first_name} {user.last_name}'] = len(DockingRecord.objects.filter(
                            Q(docked__gte = from_date) & Q(docked__lte = to_date) & Q(Q(operator1 = user) | Q(operator2 = user2))
                            )
                        )
                else:
                    users_dict[f'{user.first_name} {user.last_name}'] = len(DockingRecord.objects.filter(
                            Q(docked__gte = from_date) & Q(Q(operator1 = user) | Q(operator2 = user2))
                            )
                        )
            elif to_date:
                users_dict[f'{user.first_name} {user.last_name}'] = len(DockingRecord.objects.filter(
                        Q(docked__lte = to_date) & Q(Q(operator1 = user) | Q(operator2 = user2))
                    )
                )
        context = {
            "users_dict": users_dict,
        }
        return render(request, 'htmx/users-filtered.html', context=context)

    for user in users:
        user2 = SecondOperator.objects.get(second_operator = user)
        users_dict[f'{user.first_name} {user.last_name}'] = len(DockingRecord.objects.filter(Q(operator1 = user) | Q(operator2 = user2)))

    return users_dict

@login_required(login_url='login')
@user_passes_test(view_records)
def index(request):
    weeks_dict, filtered = filter_month(request)
    stands, stands_dict  = filter_stands(request)
    users_dict  = filter_users(request)

    context = {
        "weeks_dict":weeks_dict,
        "filtered":filtered,
        "stands": stands,
        "stands_dict": stands_dict,
        "users_dict": users_dict,
    }
    return render(request, 'index.html', context=context)
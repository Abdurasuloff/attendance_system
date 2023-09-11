from django.shortcuts import render, redirect
from datetime import date
from .models import Team, Attendance, Worker, Mark
from django.http import HttpResponse

# Create your views here.


def index(request):
    teams = Team.objects.all()
    return render(request, 'index.html', {'teams':teams})


def attendance_detail(request, team_id):
    team = Team.objects.get(id=team_id)
    is_att_taken = True if Attendance.objects.filter(date=date.today(), team=team) else False
    return render(request, "detail.html", {'team':team, "is_att_taken":is_att_taken})


def attendance_take(request, team_id):
    team = Team.objects.get(id=team_id)
    today = date.today()
    if not Attendance.objects.filter(date=today, team=team):
        if request.method == 'POST':
            attendance = Attendance.objects.create(team=team, date=today)
            marks = []
            for worker in team.workers.all():
                is_attended_input = request.POST.get(f"is_attended_{worker.id}")
                is_attended = True if is_attended_input == "on" else False
                mark = Mark(attendance=attendance, worker=worker, is_attended=is_attended)
                marks.append(mark)
            
            Mark.objects.bulk_create(marks)
            return  redirect('detail', team.id)    

                

        return render(request, 'take.html', {"team":team})
    else:
        return HttpResponse("Davomat allaqachon olib bo'lingan")
    


def attendance_update(request, attendance_id):
    attendance = Attendance.objects.get(id=attendance_id)
    if attendance.date == date.today():
        if request.method == "POST":
            marks = attendance.marks.all()
            for mark in marks:
                is_attended_input = request.POST.get(f"is_attended_{mark.id}")
                is_attended = True if is_attended_input == "on" else False
                mark.is_attended = is_attended

            Mark.objects.bulk_update(marks, ['is_attended' ,])
            return redirect("detail", attendance.team.id)
                
        return render(request, "update.html", {'attendance':attendance})
    else:
        return HttpResponse("Faqatagina bugungi olingan davomadlarni tahrirlash mumkin.")
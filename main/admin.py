from django.contrib import admin
from .models import Team, Worker, Attendance, Mark 


# Register your models here.
class WorkerInline(admin.TabularInline):
    model = Worker 

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [WorkerInline]

admin.site.register([Attendance, Worker, Mark])
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .utils import Calendar
from .forms import EventForm


def index(request):
    return HttpResponse('hello')


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM cal_Event WHERE user_id = %s", [self.request.user.id])
            result = cursor.fetchall()
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = Event.objects.raw(
            'SELECT * FROM cal_event WHERE id = %s', [event_id])[0]

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO cal_event (title, description, start_time, end_time, user_id) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                [form.cleaned_data['title'], form.cleaned_data['description'],
                    form.cleaned_data['start_time'], form.cleaned_data['end_time'], request.user.id]
            )
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'cal/event.html', {'form': form})

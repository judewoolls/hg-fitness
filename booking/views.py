from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Event, Booking
from django.views import generic
from datetime import timedelta, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EventForm

# Create your views here.

def booking(request):
    return render(request, 'booking/index.html')


def is_coach(user):
    if user.username == 'judewoolls':
        return True
    else:
        return False

@login_required
def event_detail(request, id, date):
    current_date = datetime.strptime(date, "%Y-%m-%d").date()
    queryset = Event.objects.filter(status=0, date_of_event=current_date)
    event = get_object_or_404(queryset, id=id, date_of_event=current_date)

    return render(
        request,
        "booking/event_detail.html",
        {"event": event,
         "is_coach": is_coach(request.user)}
    )


@login_required
def get_events_for_date(date):
    return Event.objects.filter(date_of_event=date).order_by('start_time')


@login_required
def event_search(request, date):
    try:
        current_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return HttpResponse("Invalid date format", status=400)

    previous_date = current_date - timedelta(days=1)
    next_date = current_date + timedelta(days=1)

    events = Event.objects.filter(date_of_event=current_date, status=0)
    events = events.order_by('start_time')
    for event in events:
        event.is_user_booked = event.is_user_booked(request.user)

    return render(request, "booking/event_search.html", {
        "events": events,
        "current_date": current_date,
        "previous_date": previous_date,
        "next_date": next_date,
        "is_coach": is_coach(request.user)
    })


# used to create a booking
def book_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        if event.is_full():
            messages.error(request, "Event is full")
            return redirect('event_search', date=event.date_of_event)

        if event.is_user_booked(request.user):
            messages.error(request, "You have already booked this event")
            return redirect('event_search', date=event.date_of_event)

        booking = Booking(event=event, user=request.user)
        booking.save()
        messages.success(request, "Event booked successfully")
        return redirect('event_search', date=event.date_of_event)
    return redirect('event_search', date=event.date_of_event)


# used to cancel a booking
def cancel_event(request, event_id):
    user = request.user
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        booking = Booking.objects.filter(event=event, user=user).first()
        if booking:
            booking.delete()
            messages.success(request, "Booking cancelled successfully")
        else:
            messages.error(request, "You do not have a booking for this event")
        return redirect('event_search', date=event.date_of_event)
    return redirect('event_search', date=event.date_of_event)


# The coach views

def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully")
        return redirect('event_search', date=event.date_of_event)
    return redirect('event_search', date=event.date_of_event)


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            messages.success(request, "Event created successfully")
            return redirect('event_search', date=event.date_of_event)
        else:
            print(form.errors)  # Debugging information
    else:
        form = EventForm()
    return render(
        request,
        "booking/create_event.html",
        {"is_coach": is_coach(request.user),
         'form': form}
    )


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, "Event updated successfully")
            return redirect('event_search', date=event.date_of_event)
        else:
            print(form.errors)  # Debugging information
    else:
        form = EventForm(instance=event)
    return render(
        request,
        "booking/edit_event.html",
        {"event": event,
         'form': form,
         "is_coach": is_coach(request.user)}
    )

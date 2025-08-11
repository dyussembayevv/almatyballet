from django.shortcuts import render, get_object_or_404
from .models import Carousel, Event, Backstage

# Create your views here.

def home(request):
    return render(request, 'index.html')

def index(request):
    slides = Carousel.objects.all()
    homepage_events = Event.objects.filter(show_on_homepage=True)[:3]
    homepage_backstages = Backstage.objects.filter(show_on_homepage=True)[:4]

    return render(request, 'index.html', {
        'slides': slides,
        'events': homepage_events,
        'backstages': homepage_backstages,
    })

def tickets(request):
    events = Event.objects.all()
    return render(request, 'tickets.html', {'events': events})

def about(request):
    backstage_items = Backstage.objects.all()  # или .filter(...) если нужно ограничить
    return render(request, 'about.html', {'backstage_items': backstage_items})

def backstage_detail(request, id):
    item = get_object_or_404(Backstage, id=id)
    return render(request, 'backstage_detail.html', {'item': item})

def event_detail(request, id):
    item = get_object_or_404(Event, id=id)
    return render(request, 'event_detail.html', {'item': item})

def support(request):
    return render(request, 'support.html')
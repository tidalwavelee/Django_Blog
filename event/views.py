from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from event.models import Event
from event.forms import EventForm

class EventsListView(ListView):
  model = Event
  paginate_by = 20
  context_object_name = "events"
  def get_queryset(self, **kwargs):
    return Event.objects.get_event(kwargs["area_code"])
  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    context["popular_tags"] = Event.objects.get_counted_tags()
    return context

class EventDetailView(DetailView):
  model = Event
  context_object_name = "event"
  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)
    event = self.get_object()
    if self.request.user.username == question.user.username:
      is_event_poster = True
    else:
      is_event_poster = False
    context["is_event_poster"] = is_event_poster
    return context

class CreateEventView(LoginRequiredMixin, CreateView):
  form_class = EventForm
  template_name = "event/event_form.html"
  message = _("Your event has been posted.")
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  def get_success_url(self):
    messages.success(self.request, self.message)
    return reverse("event:index_all")

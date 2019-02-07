from django.db import models
from django.urls import reverse
from sales.models import Sala
# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    sala_esdeveniment = models.ForeignKey(Sala, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

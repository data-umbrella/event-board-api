from django.db import models
from django.conf import settings
from django.utils.html import format_html


class Event(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    event_name = models.CharField(max_length=500, blank=False, null=True)
    description = models.TextField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    submitted= models.BooleanField(default=False)
    hash_tag = models.CharField(max_length=200, blank=True, null=True)
    conference_name = models.CharField(max_length=200, blank=True, null=True)
    organization_name = models.CharField(max_length=200, blank=True, null=True)
    acronym = models.CharField(max_length=200, blank=True, null=True)
    event_url = models.URLField(blank=True, null=True)
    organization_url = models.URLField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.CharField(max_length=200, blank=True, null=True)
    end_time = models.CharField(max_length=200, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=200, blank=True, null=True)
    in_person = models.BooleanField(blank=True, null=True)
    virtual = models.BooleanField(blank=True, null=True)
    cfp_due_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=200, blank=True, null=True)
    code_of_conduct_url = models.URLField(blank=True, null=True)
    price = models.CharField(max_length=200, blank=True, null=True)
    event_type = models.CharField(max_length=200, blank=True, null=True)
    event_notes = models.TextField(blank=True, null=True)
    volunteering_notes = models.TextField(blank=True, null=True)
    accessibility_options = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    image_file = models.ImageField(upload_to='media', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    cfp_url = models.URLField(blank=True, null=True)
    price_range = models.CharField(max_length=200, blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    timezone = models.CharField(max_length=200, blank=True, null=True)
    continent = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name
    
    def review_link(self):
        url = f"https://events.dataumbrella.org/events/{self.id}/details"
        return format_html(f'<a href="{url}" target="_blank">Review</a>', url=url)
    
    def event_link(self):
        url = f"https://events.dataumbrella.org/events/{self.id}/details"
        return format_html(f'<a href="{url}" target="_blank">{self.event_name}</a>', url=url)
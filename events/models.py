from django.db import models


class Event(models.Model):
    event_name = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    hash_tag = models.CharField(max_length=200, blank=True, null=True)
    conference_name = models.CharField(max_length=200, blank=True, null=True)
    organization_name = models.CharField(max_length=200, blank=False, null=True)
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
    price=models.CharField(max_length=200, blank=True, null=True)
    event_type=models.CharField(max_length=200, blank=True, null=True)
    event_notes = models.TextField(blank=True, null=True)
    volunteering_notes = models.TextField(blank=True, null=True)
    accessibility_options = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    image_file = models.ImageField(upload_to='media', blank=True, null=True)

    def __str__(self):
        return self.title

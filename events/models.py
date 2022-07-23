from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    featured = models.BooleanField()
    hash_tag = models.CharField(max_length=200, blank=True, null=True)
    conference_name = models.CharField(max_length=200, blank=True, null=True)
    organization_name = models.CharField(max_length=200, blank=False)
    acronym = models.CharField(max_length=200, blank=True, null=True)
    event_url = models.URLField(blank=True, null=True)
    organization_url = models.URLField(blank=True, null=True)
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)
    startTime = models.DateField(blank=True, null=True)
    endtime = models.DateField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=200, blank=True, null=True)
    in_person = models.BooleanField(blank=True, null=True)
    virtual = models.BooleanField(blank=True, null=True)
    cfp_due_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=200, blank=True, null=True)
    code_of_conduct_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

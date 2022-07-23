from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    featured = models.BooleanField()
    hash_tag = models.CharField(max_length=200, null=True)
    conference_name = models.CharField(max_length=200, null=True)
    organization_name = models.CharField(max_length=200, null=True)
    acronym = models.CharField(max_length=200, null=True)
    event_url = models.URLField(null=True)
    organization_url = models.URLField(null=True)
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    startTime = models.DateField(null=True)
    endtime = models.DateField(null=True)
    location = models.TextField(null=True)
    region = models.CharField(max_length=200, null=True)
    in_person = models.BooleanField(null=True)
    virtual = models.BooleanField(null=True)
    cfp_due_date = models.DateField(null=True)
    language = models.CharField(max_length=200, null=True)
    code_of_conduct_url = models.URLField(null=True)

    def __str__(self):
        return self.title

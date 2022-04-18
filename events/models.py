from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    featured = models.BooleanField()
    hash_tag = models.CharField(max_length=200)

    def __str__(self):
        return self.title

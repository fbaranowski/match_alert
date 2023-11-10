from django.db import models


class League(models.Model):
    name = models.CharField(max_length=100)
    href_str = models.TextField()

    def __str__(self):
        return self.name

from django.db import models


class League(models.Model):
    name = models.CharField(max_length=100)
    href_str = models.TextField()
    season = models.CharField(max_length=7, default="2023/24")

    def __str__(self):
        return self.name

from django.db import models

# Create your models here.


class Video(models.Model):
    MovieID = models.AutoField(primary_key=True)
    MovieTitle = models.CharField(max_length=200)
    Actor1Name = models.CharField(max_length=100, blank=True)
    Actor2Name = models.CharField(max_length=100, blank=True)
    DirectorName = models.CharField(max_length=100, blank=True)
    MovieGenre = models.CharField(max_length=50, blank=True)
    ReleaseYear = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.MovieTitle} ({self.ReleaseYear or 'N/A'})"
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Track(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  track_name = models.CharField(max_length=100)
  spotify_streams = models.PositiveIntegerField()
  artist = models.ForeignKey(
      'Artist',
      related_name='tracks',
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"{self.track_name}"

  def as_dict(self):
    """Returns dictionary version of Artist models"""
    return {
        'id': self.id,
        'name': self.name,
        'current_followers': self.current_followers,
        'current_monthly_listeners': self.current_monthly_listeners
    }

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Artist(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  name = models.CharField(max_length=100)
  current_followers = models.PositiveIntegerField()
  current_monthly_listeners = models.PositiveIntegerField()
  # tracks = models.ForeignKey(
  #   'Track',
  #   related_name='tracks',
  #   on_delete=models.CASCADE
  # )
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"{self.name}"

  def as_dict(self):
    """Returns dictionary version of Artist models"""
    return {
        'id': self.id,
        'name': self.name,
        'current_followers': self.current_followers,
        'current_monthly_listeners': self.current_monthly_listeners
    }

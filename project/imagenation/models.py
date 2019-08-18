from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
	tag = models.CharField(max_length=50)
	count = models.IntegerField(default=0)

	def __str__(self):
		return str(self.tag)

class Photo(models.Model):
	owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="photo_owner", blank=True, null=True)
	photo = models.FileField(blank=True)
	dtype = models.CharField(max_length=20)
	share = models.BooleanField(default=False)
	time  = models.DateTimeField()
	tags  = models.ManyToManyField(Tag)
	likes = models.IntegerField(default=0)

class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="logged_in_user")
	like_photos = models.ManyToManyField(Photo)

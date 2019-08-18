from django.db import models
from django.contrib.auth.models import User

# model for blog post
class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="post_user")
	text = models.CharField(max_length=200)
	time = models.DateTimeField()

	def __str__(self):
		return 'Post by ' + str(self.user) + ':' + self.text + '@' + str(self.time)

# model for user profile
class Profile(models.Model):
	user 			= models.ForeignKey(User, on_delete=models.PROTECT, related_name="logged_in_user")
	profile_picture	= models.FileField(blank=True)
	content_type	= models.CharField(max_length=50)
	bio 			= models.CharField(max_length=200)
	followers 		= models.ManyToManyField(User)
	
	def __str__(self):
		return 'Profile of ' + str(self.user)

# check new grading script
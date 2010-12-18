from django.db import models


class User(models.Model):
	email = models.CharField(max_length=128)
	pw_hash = models.CharField(max_length=64)
	

class Puzzle(models.Model):
	name = models.CharField(max_length=128)
	description = models.CharField(max_length=1024)
	goals = models.TextField()
	board = models.TextField()
	date_created = models.DateTimeField('date created')
	date_edited = models.DateTimeField('date last edited')
	author = models.ForeignKey(User, related_name='puzzles', null=True)

	def __unicode__(self):
		return self.name


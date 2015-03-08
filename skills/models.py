from django.db import models

# Create your models here.

class Skils(models.Model):

	def __str__(self):
		return self.skill

	skill =  models.CharField(max_length=200)
	name = models.CharField(max_length=300)
	score = models.FloatField(max_length=100)
	normalized = models.FloatField(max_length=15)
	sessionid = models.CharField(max_length=100)
	#skillid
	#noteGenDate=models.DateTimeField('note date generated')
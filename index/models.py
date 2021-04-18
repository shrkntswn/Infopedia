from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Category(models.Model):
	category = models.CharField(max_length=100)
	class Meta:
		verbose_name_plural = "categories"
	def __str__(self):
		return self.category

	'''def save(self, *args, **kwargs):
		qs = Category.objects.filter(category=self.category)
		if qs.exists():
			raise ValidationError('This category already exists')
		else:
			return super().save(*args, **kwargs)'''


class MainArticle(models.Model):
	category = models.ForeignKey(Category, related_name='mainarticle', on_delete=models.SET_DEFAULT, null=True, blank=True, default=1)
	title= models.CharField(max_length=100)
	short_description = models.CharField(max_length=500, blank=True, null=True)
	slug=models.SlugField(max_length = 250, null=False,)
	published_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self): 
		return self.title 
		
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		return super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('article_detail', args=[self.id, self.slug])



class SubArticle(models.Model):
	sub_title= models.CharField(max_length=100)
	content = models.TextField()
	image = models.ImageField(upload_to='SubArticle/', null=True, blank=True) 
	image_description = models.CharField(max_length=100, blank=True, null=True)
	sub_article = models.ForeignKey(MainArticle, on_delete=models.CASCADE)
	title_to_external_link = models.CharField(max_length=200, null=True, blank=True)
	external_link = models.URLField(max_length=300,null=True, blank=True)
	other_reference = models.CharField(max_length=200, null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
	published_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self): 
		return self.sub_title
		

class SubArticleRollBack(models.Model):
	history_of =  models.ForeignKey(SubArticle, on_delete=models.CASCADE, null=True, blank=True)
	sub_title= models.CharField(max_length=100)
	content = models.TextField()
	image = models.ImageField(upload_to='SubArticleRollBack/', null=True, blank=True) 
	image_description = models.CharField(max_length=100, blank=True, null=True)
	sub_article = models.ForeignKey(MainArticle, on_delete=models.CASCADE)
	title_to_external_link = models.CharField(max_length=200, null=True, blank=True)
	external_link = models.URLField(max_length=300,null=True, blank=True)
	other_reference = models.CharField(max_length=200, null=True, blank=True)
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
	#published_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self): 
		return str(self.updated_at) + " " + self.sub_article.title + "-" + self.sub_title
		

	def filtered_rollback(self): 
		year = self.updated_at.year*12*30
		month = self.updated_at.month*30
		day = self.updated_at.day
		total_days = year+month+day

		current_year = datetime.now().year*12*30
		current_month = datetime.now().month*30
		current_day = datetime.now().day
		total_current_days = current_year+current_month+current_day
		dt = total_current_days - total_days
		if dt < 31:
			return self.id
		else:
			self.delete()

	
		

	

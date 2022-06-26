from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from . forms import *
from django.contrib import messages
from django.core.exceptions import ValidationError
import random
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
import json
#from datetime import timedelta
#from django.utils.timezone import timezone
#from django.db.models.signals import pre_save
#from django.dispatch import receiver

from django.db.models import CharField
from django.db.models.functions import Length
from django.urls import reverse

CharField.register_lookup(Length)


categories = Category.objects.all().order_by('category')

###SEARCH PAGE
def search(request):
	global categories

	query = request.GET.get('search')
	if query:
		related_articles={}
		try: # if there is only one article with that name, then itwill return that
			article = MainArticle.objects.get(title__istartswith=query) #_iexact exactly matches the word with case insensitive
			return redirect('article_detail', article.id, article.slug)
		except:
			articles = MainArticle.objects.filter(title__istartswith=query).order_by('title')# if there are many articles starting with same name
			if articles: # if the list is not empty containing istartswith query
				articles = articles 
			else:
				articles = MainArticle.objects.filter(title__iexact = query) # if none of the article matches starting with same name then it will look for article containing that query string
				if articles.count() == 1:
					article = articles[0]    # if only one article found then it will return that
					return redirect('article_detail', article.id, article.slug)
				    # else it will return related articles 
			related_articles=list(set(MainArticle.objects.filter(title__icontains=query, title__length__gt=2))-set(MainArticle.objects.filter(title__istartswith=query)))
			context={'articles':articles,'categories':categories, 'query':query,'search_title':"Search", 'related_articles':related_articles}
	else:
		context={'categories':categories, 'search_title':"Search"}
	return render(request, 'index/articles/search.html', context)


#AUTO COMPLETE
def auto_search(request):
	if request.is_ajax():
		query = request.GET.get('term') #use 'term' word only ...no other word for jquery autocomplete
		qs = MainArticle.objects.filter(title__istartswith = query).order_by('title')
		if qs:
			qs = qs
		elif MainArticle.objects.filter(title__iexact = query):
			qs = MainArticle.objects.filter(title__iexact = query).order_by('title')
		else:
			qs = MainArticle.objects.filter(title__icontains = query)
		results = []
		for article in qs:
			article_json ={}
			article_json['label'] = article.title
			article_json['url'] = article.get_absolute_url()
			results.append(article_json)
			print(results)	
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)


###Category Filter Page
def category(request, id, category):
	global categories
	articles = MainArticle.objects.filter(category__id=id)
	context = {'articles':articles, 'categories':categories, 'category_title':"Category-"+str(category)}
	return render(request, 'index/articles/category.html', context)


### HOME PAGE
def home(request):
	global categories 
	articles = MainArticle.objects.all().order_by('-published_at')
	random_article = random.choice(articles)
	context={'articles':articles, 'home_title':"Home",'categories':categories, 'random_article':random_article}
	return render(request, 'index/articles/home.html', context)

### RANDOM ARTICLE
def random_article(request):
	articles = MainArticle.objects.all().order_by('-published_at')
	random_article = random.choice(articles)
	return redirect('article_detail', random_article.id, random_article.slug)


### ARTICLE DETAIL PAGE
def article_detail(request, id, slug):
	global categories
	article=get_object_or_404(MainArticle, id=id)
	sub_articles = SubArticle.objects.filter(sub_article=article)
	context={'article':article, 'sub_articles':sub_articles, 'article_detail_title':str(article.title[:50]),'categories':categories}
	return render(request, 'index/articles/article_detail.html', context)


### ADD NEW CATEGORY
def add_category(request):
	category_form=CategoryCreationForm()
	if request.method=='POST':
		category_form=CategoryCreationForm(data=request.POST)
		if category_form.is_valid():
			category_form.save()
	return redirect('main_article_create')


### CREATING MAIN ARTICLE
def main_article_create(request, *args):
	global categories
	category_form=CategoryCreationForm()
	form = MainArticleCreationForm()
	if request.method == 'POST':
		form = MainArticleCreationForm(data=request.POST)
		if form.is_valid():
			post=form.save(commit=False)
			post.title=post.title.capitalize()
			post.published_at=datetime.now()
			post.save()
			return redirect('sub_article_create', post.id )
	context={'form':form,'main_article_create_title':"Create",'category_form':category_form,'categories':categories}
	return render(request, 'index/articles/main_article_create.html', context)


### CREATING SUB ARTICLE
def sub_article_create(request, id,):
	global categories
	main_article = get_object_or_404(MainArticle, id=id)
	sub_articles = SubArticle.objects.filter(sub_article__id=main_article.id)
	form = SubArticleCreationForm()
	if request.method == 'POST':
		form = SubArticleCreationForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			post=form.save(commit=False)
			post.sub_article = main_article
			post.published_at = datetime.now()
			post.save()
			return redirect('sub_article_create', id)
	context={'form':form, 'main_article':main_article, 'sub_articles':sub_articles, 'sub_article_create_title':"Add Details-"+str(main_article.title),'categories':categories}
	return render(request, 'index/articles/sub_article_create.html', context)


### UPDATING MAIN ARTICLE 
def article_update(request, id):
	global categories
	main_article=get_object_or_404(MainArticle, id=id)
	form = MainArticleCreationForm(instance=main_article)
	sub_articles = SubArticle.objects.filter(sub_article__id=main_article.id)
	if request.method == 'POST':
		form = MainArticleCreationForm(data=request.POST, instance=main_article)
		if form.is_valid():	
			post=form.save()
			return redirect('sub_article_create', post.id)
	context={'form':form,'categories':categories, 'main_article_update_title':"Edit-"+str(main_article.title[:50]),'main_article':main_article}
	return render(request, 'index/articles/main_article_update.html', context)


### UPDATE SUB ARTICLES
def sub_article_update(request, id):
	global categories
	rollbacks_old = SubArticleRollBack.objects.filter(history_of__id=id).order_by('-updated_at')
	rollbacks=[]
	for rollback in rollbacks_old:
		if not rollback.filtered_rollback():
			rollbacks
		else:
			rollbacks.append(rollback)
	sub_article=get_object_or_404(SubArticle, id=id)
	
	form = SubArticleCreationForm(instance=sub_article)
	if request.method == 'POST':
		form = SubArticleCreationForm(data=request.POST, files=request.FILES, instance=sub_article)
		history=sub_article_history_save(sub_article)
		if form.is_valid():
			post=form.save()
			return redirect('article_detail', sub_article.sub_article.id, sub_article.sub_article.slug)
		else:
			history.delete()
	context={'form':form,'sub_article_update_title':"Edit-"+str(sub_article.sub_title[:50]),'categories':categories, "sub_article":sub_article, 'rollbacks':rollbacks}
	return render(request, 'index/articles/sub_article_update.html', context)

### SAVE SUB ARTICLE HISTORY
def sub_article_history_save(instance):
	sub_article_history = SubArticleRollBack.objects.create(
		history_of = instance,
		sub_title = instance.sub_title,
		content = instance.content,
		image = instance.image,
		image_description = instance.image_description,
		sub_article = instance.sub_article,
		title_to_external_link = instance.title_to_external_link,
		external_link = instance.external_link,
		other_reference = instance.other_reference,
		)
	return sub_article_history

### SAVE ROLLBACK
def rollback(request, id):
	sub_article=get_object_or_404(SubArticle, id=id)
	rollback_id = request.GET.get('rollback') 
	rollback = get_object_or_404(SubArticleRollBack, id=rollback_id)
	sub_article.sub_title = rollback.sub_title
	sub_article.content = rollback.content
	sub_article.image = rollback.image
	sub_article.image_description = rollback.image_description
	sub_article.title_to_external_link = rollback.title_to_external_link
	sub_article.external_link = rollback.external_link
	sub_article.other_reference = rollback.other_reference
	sub_article.save()
	"""sub_article.save(update_fields=['sub_title',
					'content',
					'image',
					'image_description',
					'title_to_external_link',
					'external_link',
					'other_reference',])"""
	return redirect('sub_article_update', id)


## DELETE MAIN ARTICLE
def article_delete(request, id):
	article = get_object_or_404(MainArticle, id=id)
	article.delete()
	context={}
	return redirect('main_article_create')

## DELETE SUB ARTICLE
def sub_article_delete(request, id, art_id, slug):
	subarticle = get_object_or_404(SubArticle, id=id)
	subarticle.delete()
	context={}
	return redirect('article_detail', art_id, slug)
	
	#return HttpResponseRedirect(reverse('article_detail'))


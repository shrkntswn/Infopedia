from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from ckeditor.widgets import CKEditorWidget



class CategoryCreationForm(forms.ModelForm):
	category = forms.CharField()
	class Meta:
		model=Category
		fields = ('category',)


class MainArticleCreationForm(forms.ModelForm):
	category = forms.Select()
	title = forms.CharField()
	short_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':6,}), required=False)
	class Meta:
		model=MainArticle
		fields=('category','title','short_description')


class SubArticleCreationForm(forms.ModelForm):
	content = forms.CharField(widget=CKEditorWidget())
	external_link = forms.CharField(widget=forms.URLInput(attrs={'class': 'form-control',}), required=False)
	class Meta:
		model=SubArticle
		fields=('sub_title', 'content','title_to_external_link','external_link', 'other_reference','image', 'image_description')
		

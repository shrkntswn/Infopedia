from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from .models import *


class SubArticleAdminForm(forms.ModelForm):
	content = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = SubArticle
		fields = '__all__'

class SubArticleAdmin(admin.ModelAdmin):
	form = SubArticleAdminForm
	list_display = ('sub_title', 'content',)

class MainArticleAdmin(admin.ModelAdmin):
	list_display = ('title','short_description')
	prepopulated_fields = {'slug': ('title',)}


admin.site.register(MainArticle, MainArticleAdmin)
admin.site.register(SubArticle, SubArticleAdmin)
admin.site.register(Category)
admin.site.register(SubArticleRollBack)


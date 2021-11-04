from django import forms
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django_comments_xtd.models import XtdComment
from django_extensions.db.fields import AutoSlugField
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
#from django.utils.tranlation import gettext_lazy as _

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable, PageManager, PageQuerySet
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import *
from wagtail.admin.edit_handlers import (
	FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel, StreamFieldPanel, ObjectList, TabbedInterface
)
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.forms import WagtailAdminModelForm, WagtailAdminPageForm
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.embeds.models import Embed
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.search import index
from wagtail.api import APIField

from rest_framework.fields import Field
from ckeditor import fields as ckedit
from wagtailcaptcha.models import WagtailCaptchaEmailForm
#from wagtailstreamforms.blocks import WagtailFormBlock
# from wagtailcodeblock.blocks import CodeBlock
# from wagtailtrans.models import TranslatablePage

from core.streams.blocks import *
#from core.streams.choices import *
from core.blog.models import *
from core.store.models import *
from core.site_settings.models import *
from core.menus.models import *

from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox 

META_ROBOTS_CHOICE = [
	("index, folllow","Index, Follow"),
	("index, nofollow","Index, Nofollow"),
	("noindex, follow","Noindex, Follow"),
	("noindex, nofollow","Noindex, Nofollow"),
]

META_LANGUAGES = [
    ('en', "English"),
    ('es', "Español"),
    ('fr', "Français"),
    ('de', "Deutsch"),
    ('nl', "Nederlands"),
    ('pt', "Portuguese"),
]

class FormWithCaptcha(forms.Form):
	captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class OfertasEspeciales(Orderable):
	nombre = models.CharField("Name", blank=False, null=True, max_length=150)
	imagen_destacada = models.ForeignKey("wagtailimages.Image", verbose_name="Thumbnail Image", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
	texto = models.TextField("Text Comment", blank=True, null=True)
	product_url = models.URLField("URL", max_length=500, blank=True, null=True)
	#disponible = models.BooleanField(default=True,)
	relevant_section_title = models.CharField(blank=False, null=True, max_length=500)
	relevant_section_comment = models.TextField(blank=True, null=True)
	
	
	page = ParentalKey("HomePage", related_name="ofertas_especiales", null=True)

	panels = [
		FieldPanel("nombre"),
		ImageChooserPanel("imagen_destacada"),
		FieldPanel("texto"),
		FieldPanel("product_url"),
		#FieldPanel("disponible"),
	]

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Relevant Content"
		verbose_name_plural = "Relevants"


class HomePage(Page):
	template = 'home/home_page.html'
	#parent_page_type = ['wagtailcore.Page'] # appname.ModelName
	# subpage_types = ['blog.BlogSinglePage', 'contact.FormPage'] # appname.ModelName
	search_auto_update = False
	max_count = 1

# Header Panel
	imagen_destacada = models.ForeignKey("wagtailimages.Image", verbose_name="Main Image", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
	main_title_of_the_page = models.CharField(max_length=350, blank=False, null=True, help_text='HTML "<h1>" Tag')
	header_subtitle = models.CharField(max_length=500, blank=True, null=True)

# Promote Panel
	alert_about_cookies = models.BooleanField(default=False, null=True, blank=True)
	meta_language = models.CharField(max_length=2, choices=META_LANGUAGES, blank=True, null=True, help_text="Select in what language the content of this page is. Default is 'en'.")
	meta_keywords = models.TextField(blank=True, null=True, help_text="All your keywords you add here, must to be in your content.")
	meta_revisit_after = models.PositiveIntegerField(blank=True, null=True, default="365", help_text="Select how many days Google Spiders could revisit this page. Default is 365 days.")
	meta_robots = models.CharField(max_length=17, blank=True, null=True, choices=META_ROBOTS_CHOICE, help_text="Deside if this page will be Indexed and/or Followed by the Google Spiders. Default is 'index, follow'.")

# Content Order
	CONTENT_ORDER_CHOICES = [
		("cc", "Categorized Cards"),
		("rl", "Relevants"),
		("ct", "Custom Content"),
	]
	show_at_the_beg =  models.CharField("Show at the Beginning", unique=True, max_length=2, default="cc", choices=CONTENT_ORDER_CHOICES, blank=True, null=True)
	show_in_midl =  models.CharField("Show in the Middle", unique=True, max_length=2, default="rl", choices=CONTENT_ORDER_CHOICES, blank=True, null=True)
	show_at_the_end =  models.CharField("Show at the End", unique=True, max_length=2, default="ct", choices=CONTENT_ORDER_CHOICES, blank=True, null=True)
	

# Content Panel
	relevant_name = models.CharField("Relevant Section Main Title", max_length=150, blank=True, null=True)
	relevant_comment = models.TextField("Relevant Section Main Comment", blank=True, null=True)
	newsletter_title = models.CharField("Newsletter Title", max_length=150, blank=True, null=True)
	newsletter_comment = models.TextField("Newsletter Comment", blank=True, null=True)
	content = StreamField(
		[
			("intro_home", IntroSectionBGImageCentederTextBlock()),
			("custom_html", CustomHTML()),
			("divider", DividerBlock()),
			("accordion", ColapsibleBlock()),
			("summary", SummaryBlock()),
			("icon_link", CardWithIconBlock()),
			('counter_up', CountersBlock()),
			('img_info_bar', InfoBlock()),
			("pricing_card", PricingCardsBlock()),
			("jumbotron", JumbotronBlock()),
			#("contactmap", ContactMapBlock()),
		],
		null=True,
		blank=True,
	)

	content_panels = Page.content_panels + [
		FieldPanel("relevant_name"), 
		FieldPanel("relevant_comment"), 
		InlinePanel("ofertas_especiales", label="Relevant"),
		MultiFieldPanel([
			StreamFieldPanel("content"),
		], heading="Main Content"),
		FieldPanel("newsletter_title"), 
		FieldPanel("newsletter_comment"), 
	]


	content_order_panels = [
		MultiFieldPanel([
			FieldPanel("show_at_the_beg"),
			FieldPanel("show_in_midl"),
			FieldPanel("show_at_the_end"),
		], heading="Content Order"),
	]

	header_panels = [
		MultiFieldPanel([
			FieldPanel("main_title_of_the_page"),
			FieldPanel("header_subtitle"),
			ImageChooserPanel("imagen_destacada"),
		], heading="Header Section"),
	]

	promote_panels = Page.promote_panels + [
		MultiFieldPanel([
			FieldPanel("alert_about_cookies"),
			FieldPanel("meta_language"),
			FieldPanel("meta_keywords"),
			FieldPanel("meta_revisit_after"),
			FieldPanel("meta_robots"),
		], heading="Search Engine Optimization settings.")
	]

	edit_handler = TabbedInterface([
		ObjectList(header_panels, heading="Header Section"),
		ObjectList(content_panels, heading="Content"),
		ObjectList(content_order_panels, heading="Content Order"),
		ObjectList(promote_panels, heading="Promote"),
		ObjectList(Page.settings_panels, heading="Settings"),
	])

#	search_fields = Page.search_fields + [
#        index.SearchField('main_title_of_the_page'), # These are used for performing full-text searches on your models, usually for text fields.
#        index.FilterField('header_subtitle'), # These are added to the search index but are not used for full-text searches
 
#    	 index.RelatedFields('author', [ # This allows you to index fields from related objects. It works on all types of related fields
#            index.SearchField('name'),
#            index.FilterField('date_of_birth'),
#        ]),
#    ]

	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		context['items'] = Item.objects.all().distinct()
		#context['provincias'] = Provincia.objects.all()
		context['categoria_y_tipo'] = ItemCategory.objects.all()
		context['nav2categories'] = ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').all()
		context['countcatgnav2'] = ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').count()
		context['categories'] = ItemCategory.objects.all()
		#context['hora_reservaciones'] = HorasDeReservaciones.objects.all()
		context['captcha'] = FormWithCaptcha

		all_posts = BlogSinglePage.objects.live().public().order_by('-first_published_at').distinct()

		if request.GET.get('tag', None):
			tags = request.GET.get('tag')
			all_posts = all_posts.filter(tags__slug__in=[tags])
			
		# Pagination
		paginator = Paginator(all_posts, 3) # Determines how many post show for page
		page = request.GET.get("page") # "page" is a name that you can change if you want ?page={{post.previous_page_number}}
		try:
			posts = paginator.page(page)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages)

		context['posts'] = posts # BlogSinglePage.objects.live().public().order_by('-first_published_at')
		context['all_categories'] = BlogCategory.objects.all()
		
		return context

	class Meta:
		verbose_name = 'Home Page'
		verbose_name_plural = 'Home Pages'

######################   SITE_SETTINGS ########################
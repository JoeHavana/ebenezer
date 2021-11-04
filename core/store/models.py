import datetime
import allauth.app_settings
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from ckeditor import fields as ckedit
# from django_extensions.db.fields import AutoSlugField 
#from django.contrib.auth.models import User
#import requests  To work with class Latitude

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable, PageManager, PageQuerySet
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks import *
from wagtail.admin.edit_handlers import (
	FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel, StreamFieldPanel, ObjectList, TabbedInterface
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from django.db.models.signals import (
	post_delete, # Used
	post_init, 
	post_migrate,
	post_save,
	pre_save, 
	pre_delete,
	pre_init,
	m2m_changed, 
)
from django.shortcuts import reverse
#from django.dispatch import receiver, signals # No-Used
from core.streams.blocks import *
#from core.streams.choices import *


today = datetime.date.today()
now = datetime.datetime.now()



# Not in DjustDjango
class ItemImages(Orderable):
	image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
	alternative_text = models.CharField(verbose_name="Alt", max_length=150, blank=True, null=True)

	page = ParentalKey("Item", related_name="images_of_item")

	panels = [
		MultiFieldPanel([
			ImageChooserPanel("image"),
			FieldPanel("alternative_text"),
		], heading="Menu Simple de Artículo")
	]

	def __str__(self):
		return self.image.title

	class Meta:
		verbose_name = "Imagen Destacada"
		verbose_name_plural = "Imágenes Destacadas"

# from justdj => Category
class ItemCategory(models.Model):
	category_name = models.CharField(unique=True, blank=False, null=True, max_length=150, editable=True, help_text="Name must be shorts. If you would like to give extra information, fill out in 'Category description'.")
	slug =  models.CharField(unique=True, blank=False, null=True, max_length=150, editable=True, help_text="Slug have to be unique")
	category_description = models.TextField("Descripción", blank=True, null=True, help_text="Small description about this category")
	#tags_related = models.ManyToManyField("store.ItemTag", related_name="+", blank=True, help_text="Las etiquetas ayudarán a los usuarios a la hora de hacer búsquedas")
	image_related = models.ForeignKey("wagtailimages.Image", null=True, blank=True, related_name="+", on_delete=models.CASCADE)
	image_description = models.CharField(blank=True, null=True, max_length=150, editable=True, help_text="A small description describing the 'Image Reated'. This is very important for the Google'Search Engine Optimization (SEO).")
	priority = models.PositiveIntegerField(unique=True, default=1, editable=True)
	will_be_recomended = models.BooleanField("Will be recomended in the navigation pills?", default=False, blank=True, null=True)
	
	items_related = models.ManyToManyField("Item", verbose_name="Cards Related", related_name="+", blank=True, editable=True)

	panels = [
		MultiFieldPanel([
			FieldPanel("category_name"),
			FieldPanel("category_description"),
			ImageChooserPanel("image_related"),
			FieldPanel("image_description"),
			FieldPanel("priority"),
			FieldPanel("will_be_recomended"),
			FieldPanel("slug"),
		], heading="Card Categories")
	]

	def __str__(self):
		return self.category_name

	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Card Categories"

	def get_absolute_url(self):
		return reverse("category-detail", kwargs={ "slug":self.slug }) # core = appname; product is my url_name, in urls.py


# In JustDjango (Extended)
class Item(ClusterableModel):
	title = models.CharField("Card Title", max_length=100, editable=True, unique=True)
	slug = models.SlugField(editable=True, unique=True, help_text="Slugs must be uniques")
	short_description = models.TextField(blank=True, null=True)
	full_description = ckedit.RichTextField("Card full content", blank=True, null=True)
	main_picture_of_presentation = models.ForeignKey("wagtailimages.Image", verbose_name="Thumbnail Image", on_delete=models.SET_NULL, null=True, blank=False, related_name="+")
	categories = models.ManyToManyField(ItemCategory, verbose_name="Categories related", blank=True, help_text="Select if exists one or more categories related to this Item. Press 'CTRL' to select multiple.")
	
	internal_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True, related_name="+", on_delete=models.SET_NULL)
	URL = models.URLField(blank=True, null=True)
	open_in_a_new_tab = models.BooleanField(default=False, help_text='Default is "No"', blank=True, null=True)
	rel_attribute = models.CharField(max_length=150, blank=True, null=True)
	
	or_automate_a_page = models.BooleanField(default=True, blank=True, null=True, help_text="Will auto-generate the a page with the content")

	panels = [
		MultiFieldPanel([
			FieldPanel("title"),
			FieldPanel("slug"),
			FieldPanel("short_description"),
			FieldPanel("full_description"),
		], heading="Main Data"),
		MultiFieldPanel([
			PageChooserPanel("internal_page"),
			FieldPanel("URL"),
			FieldPanel("open_in_a_new_tab"),
			FieldPanel("rel_attribute"),
			FieldPanel("or_automate_a_page"),
		], heading="Link Settings"),
		MultiFieldPanel([
			ImageChooserPanel("main_picture_of_presentation"),
			InlinePanel("images_of_item", label="Images Related"),
		], heading="Imágenes"),
		MultiFieldPanel([
			FieldPanel("categories"),
		], heading="Categories"),
	]

	def __str__(self):
		return self.title
		
	class Meta:
		verbose_name = 'Card'
		verbose_name_plural = 'Cards'

	def get_absolute_url(self):
		return reverse("product-detail", kwargs={ "slug":self.slug })

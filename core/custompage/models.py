from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core.blocks import *
from wagtail.admin.edit_handlers import (
	FieldPanel, MultiFieldPanel, ObjectList, TabbedInterface
)
from wagtail.images.edit_handlers import ImageChooserPanel
from core.streams.blocks import *
#from core.streams.choices import *
from core.blog.models import *
from core.store.models import *
from core.site_settings.models import *
from core.menus.models import *


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

class CustomPage(Page):
	template = 'custompage/custom_page.html'
	#parent_page_type = ['home.HomePage'] # appname.ModelName
	#subpage_types = ['blog.BlogSinglePage', 'contact.FormPage'] # appname.ModelName
	search_auto_update = False

# Header Panel
	imagen_destacada = models.ForeignKey("wagtailimages.Image", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
	main_title_of_the_page = models.CharField(max_length=350, blank=False, null=True, help_text='HTML "<h1>" Tag')
	header_subtitle = models.CharField(max_length=500, blank=True, null=True)

# Promote Panel
	alert_about_cookies = models.BooleanField(default=False, null=True, blank=True)
	meta_language = models.CharField(max_length=2, choices=META_LANGUAGES, blank=True, null=True, help_text="Select in what language the content of this page is. Default is 'en'.")
	meta_keywords = models.TextField(blank=True, null=True, help_text="All your keywords you add here, must to be in your content.")
	meta_revisit_after = models.PositiveIntegerField(blank=True, null=True, default="365", help_text="Select how many days Google Spiders could revisit this page. Default is 365 days.")
	meta_robots = models.CharField(max_length=17, blank=True, null=True, choices=META_ROBOTS_CHOICE, help_text="Deside if this page will be Indexed and/or Followed by the Google Spiders. Default is 'index, follow'.")


# Content Panel
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
			("contactmap", ContactMapBlock()),
		],
		null=True,
		blank=True,
	)

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			StreamFieldPanel("content"),
		], heading="Main Content"),
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
		ObjectList(promote_panels, heading="Promote"),
		ObjectList(Page.settings_panels, heading="Settings"),
	])


	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		context['items'] = Item.objects.all().distinct()
		context['categoria_y_tipo'] = ItemCategory.objects.all()
		context['nav2categories'] = ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').all()
		context['countcatgnav2'] = ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').count()

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
		verbose_name = 'Custom Page'
		verbose_name_plural = 'Custom Pages'



class StaticPage(Page):
	template = 'staticpage/static_page.html'
	custom_css = models.TextField("Custom CSS", blank=True, null=True, help_text="Paste the CSS code, including <style></style> tags.")
	custom_JavaScript = models.TextField("Custom JavaScript", blank=True, null=True, help_text="Paste the JS code, including <script></script> tags.")
	html_content = models.TextField("Custom HTML", blank=False, null=True, help_text="Paste the HTML code. Will be rendered inside <body> ( your html ) </body> tags.")

	content_panels = Page.content_panels + [
		FieldPanel("custom_css"),
		FieldPanel("custom_JavaScript"),
		FieldPanel("html_content"),
	]

	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		return context

	class Meta:
		verbose_name = 'Static Page'
		verbose_name_plural = 'Static Pages'
		
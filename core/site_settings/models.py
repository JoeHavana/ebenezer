from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.models import ClusterableModel
from wagtail.core.models import Page, Orderable, PageManager, PageQuerySet
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField, StreamField
from core.streams.blocks import *

SOCIALLINKS_CHOICES = [
    ('Fc', 'Facebook'),
    ('Ig', 'Instagram'),
    ('Li', 'LinkedIn'),
    ('Pt', 'Pinterest'),
    ('Ptr', 'Patreon'),
    ('Snp', 'Snapchat'),
    ('Tw', 'Twitter'),
    ('Vm', 'Vimeo'),
    ('Xi', 'Xing'),
    ('Yp', 'Yelp'),
    ('Yt', 'YouTube'),
]

@register_setting
class FromGoogle(BaseSetting):
    gmail_user_account = models.TextField(unique=True, blank=True, null=True, editable=True)
    gmail_password = models.TextField(unique=True, blank=True, null=True, editable=True)
    google_analytics = models.TextField(unique=True, blank=True, null=True, editable=True, help_text="Copy and Paste here the Scripts provided by your Google Analytics.")
    google_adsense = models.TextField(unique=True, blank=True, null=True, editable=True, help_text="Copy and Paste here the Scripts provided by your Google Ads.")
    google_maps_iframe = models.TextField(unique=True, blank=True, null=True, editable=True, help_text="Copy and Paste here the iFrame provided by Google Maps.")
    
    panels = [
        FieldPanel("gmail_user_account"),
        FieldPanel("gmail_password"),
        FieldPanel("google_analytics"),
        FieldPanel("google_adsense"),
        FieldPanel("google_maps_iframe"),
    ]

    class Meta:
        verbose_name = 'Data connections with Google'


class SocialNetworkBrand(Orderable):
    social_net_icon = models.CharField("Social Network", max_length=500, blank=True, null=True, choices=SOCIALLINKS_CHOICES, help_text="Select a Social NetWork.")
    url = models.URLField(max_length=500, blank=True, null=True)

    page = ParentalKey("Brand", related_name="social_items", null=True)

    panels = [
        FieldPanel("social_net_icon"),
        FieldPanel("url"),
    ]

@register_setting
class Brand(ClusterableModel, BaseSetting):
    favicon_image = models.ForeignKey("wagtailimages.Image", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    brand_image_logo = models.ForeignKey("wagtailimages.Image", verbose_name="Logo", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    brand_name = models.CharField("Church Name", max_length=50, blank=True, null=True, unique=True, editable=True)
    show_logo_image = models.BooleanField("Show Logo", default=False, blank=True, null=True)
    show_brand_name = models.BooleanField("Show Name", default=True, blank=True, null=True, help_text='If "Logo" is selected to be shown, then DO NOT select the "Church Name".')

    public_email = models.EmailField("Public Email", blank=True, null=True, help_text="This Email will be public, used for communication with the users.")
    public_phone = models.PositiveIntegerField("Public Phone Number", blank=True, null=True, help_text="This phone number will be public, used for communication with the users.")
    business_directions = models.TextField("Location", blank=True, null=True, help_text="This address will be shown in the website.")
    extra_data = models.TextField("Extra Data", blank=True, null=True)

    panels = [
        MultiFieldPanel([
            ImageChooserPanel("favicon_image"),
            ImageChooserPanel("brand_image_logo"),
            FieldPanel("brand_name"),
            FieldPanel("show_logo_image"),
            FieldPanel("show_brand_name"),
            FieldPanel("public_email"),
            FieldPanel("public_phone"),
            FieldPanel("business_directions"),
            FieldPanel("extra_data"),
            InlinePanel("social_items", label="Social Networks"),
        ], heading="Data"),
    ]

    class Meta:
        verbose_name = 'Information'


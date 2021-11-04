from django.db import models
from django.core.mail import send_mail, EmailMultiAlternatives
from wagtail.core.fields import RichTextField, StreamField
from modelcluster.models import ClusterableModel
from wagtail.core.models import Page, Orderable, PageManager, PageQuerySet
from wagtail.admin.edit_handlers import (
	FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel, StreamFieldPanel, ObjectList, TabbedInterface
)
from core.site_settings.models import Brand


class NewsletterUser(models.Model):
	name = models.CharField("Username", max_length=100, blank=True, null=False, help_text='Name')
	email = models.CharField("Email", max_length=100, blank=False, null=False, help_text='Email (required)')
	email_verified = models.BooleanField(default=False)
	date_added = models.DateTimeField("Created at:", auto_now_add=True)

	def __str__(self):
		return self.email

	def get_email(self):
		return self.email

	class Meta:
		verbose_name = "Subscriber"
		verbose_name_plural = "Subscribers"


class Newsletter(ClusterableModel):
	EMAIL_STATUS_CHOICES = [
		('Draft', 'Draft'),
		('Publish', 'Sent'),
	]
	ACTIONS_DONE_CHOICES = [
		('save', 'Save as Draft'),
		('sent', 'Send Now'),
	]
	subject = models.CharField(max_length=250, blank=True, null=True)
	body = models.TextField("Message", blank=True, null=True)
	#body = RichTextField("Mensaje", blank=True, null=True, features=['h1', 'h2', 'h3', 'h4', 'h5','h6', 'center', 'right', 'left', 'bold', 'italic', 'link', 'ol', 'ul', 'hr','document-link', 'image', 'embed', 'code', 'superscript', 'subscript', 'strikethrough', 'blockquote'])
	#email = models.ManyToManyField(NewsletterUser, blank=True)
	status = models.CharField("Status", max_length=10, choices=EMAIL_STATUS_CHOICES, default='Draft', blank=True, null=True, editable=False)
	action = models.CharField("Action to do:", max_length=10, choices=ACTIONS_DONE_CHOICES, default='save', blank=True, null=True)
	created = models.DateTimeField("Created at:", auto_now_add=True, null=True)
	updated = models.DateTimeField("Updated at:", auto_now=True, null=True)

	panels = [
		MultiFieldPanel([
			FieldPanel("subject"),
			FieldPanel("body"),
			FieldPanel("action"),
		])
	]

	def save(self, *args, **kwargs):
		if self.action == "sent":
			try:
				self.status = "Publish"
				super(Newsletter, self).save(*args, **kwargs)
				subject = self.subject
				body = self.body
				from_email = Brand.objects.first()
				from_email = from_email.public_email
				for email in NewsletterUser.objects.all():	#newsletter.email.all():
					send_mail(subject=subject, from_email=from_email, recipient_list=[email.email], message=body, fail_silently=False)
			except Exception as e:
				print("=====================================")
				print(e)
				pass

		elif self.action == "save":
			self.status = "Draft"
			super(Newsletter, self).save(*args, **kwargs)

	def __str__(self):
		return self.subject

	class Meta:
		ordering = ['subject']
		verbose_name = "Newsletter"
		verbose_name_plural = "Newsletters"

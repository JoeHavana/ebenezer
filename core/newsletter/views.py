from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.core.models import Site
from core.site_settings.models import Brand
from django import forms
from crispy_forms.helper import FormHelper
from .models import *


class NewsletterUserSignUpForm(forms.ModelForm):
	helper = FormHelper()
	helper.form_show_labels = False

	class Meta:
		model = NewsletterUser
		fields = ['name', 'email']	# 'name'

		def clean_email(self):
			email = self.cleaned_data.get('email')

			return email


class NewsletterCreationForm(forms.ModelForm):

	class Meta:
		model = Newsletter
		fields = ['subject', 'body', 'action']

		

def newsletter_signup(request):
	form = NewsletterUserSignUpForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		if NewsletterUser.objects.filter(email=instance.email).exists():
			context = {
				'form': form,
			 	'email_already_exists': True,
			}
			return render(request, "newsletter/newsletter_signup.html", context)
		else:
			instance.save()

			url_root = Site.objects.first()
			host = url_root.hostname
			human_readable_site = url_root.site_name
			# Sending email. Newsletter Cap 30
			subject = "Gracias por unirse ha nuestro Newsletter"
			from_email = Brand.objects.first()
			from_email = from_email.public_email
			to_email = [instance.email]	# email a ser enviado
			message =  f'Bienvenido. Si en algún momento desea cancelar su suscripcion, hágalo aquí:\n { host }/newsletter-unsubscribe/'
			send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=message, fail_silently=False)


			messages.info(request, "Suscrito a nuestro Newsletter")
			return redirect("/")

	context = {
		'form': form
	}
	template = "newsletter/newsletter_signup.html"
	return render(request, template, context)

def verify_email(request):
	pass

def newsletter_unsubscribe(request):
	form = NewsletterUserSignUpForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		if NewsletterUser.objects.filter(email=instance.email).exists():
			NewsletterUser.objects.filter(email=instance.email).delete()

			# Sending email. Newsletter Cap 30
			subject = "Usted ha cancelado su suscripción a nuestras publicaciones"
			from_email = Brand.objects.first()
			from_email = from_email.public_email
			to_email = [instance.email]
			message = """ Es una lástima verle ir. Déjenos saber si el motivo ha sido un mal servicio nuestro. """
			send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=message, fail_silently=False)

			messages.info(request, "Su suscripción a nuestras publicaciones ha sido cancelada.")
			return redirect("/")
			#context = {
			#	'form': form,
			# 	'unsubscribed': True,
			#}
			#return render(request, "newsletter/newsletter_unsubscribe.html", context)
		else:
			context = {
				'form': form,
			 	'not_subscribed': True,
			}
			return render(request, "newsletter/newsletter_unsubscribe.html", context)

	context = {
		'form': form
	}
	template = "newsletter/newsletter_unsubscribe.html"
	return render(request, template, context)

def control_newsletter(request):
	form = NewsletterCreationForm(request.POST or None)

	if form.is_valid():
		instance = form.save()
		newsletter = Newsletter.objects.get(id=instance.id)
		if newsletter.status == "Publish":
			subject = newsletter.subject
			body = newsletter.body
			from_email = Brand.objects.first()
			from_email = from_email.public_email
			for email in NewsletterUser.objects.all():	#newsletter.email.all():
				send_mail(subject=subject, from_email=from_email, recipient_list=[email.email], message=body, fail_silently=False)

	context = {
		'form': form,
		'emails': NewsletterUser.objects.all()
	}
	template = "newsletter/control_newsletter.html" # "newsletter/compose.html"
	return render(request, template, context)


def newsletter_list(request):
	newsletters = Newsletter.objects.all()

	paginator = Paginator(newsletters, 10)
	page = request.GET.get('page')

	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)

	index = items.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]

	context = {
		"items": items,
		"page_range": page_range
	}

	return render(request, "newsletter/list_newsletters.html", context)

def newsletter_detail(request, pk):
	newsletter = get_object_or_404(Newsletter, pk=pk)

	context = {
		"newsletter": newsletter
	}
	return render(request, "newsletter/newsletter-detail.html", context)

def newsletter_edit(request, pk):
	newsletter = get_object_or_404(Newsletter, pk=pk)

	if request.method == 'POST':
		form = NewsletterCreationForm(request.POST, instance=newsletter)

		if form.is_valid():
			newsletter = form.save()

			if newsletter.status == 'Publish':
				subject = newsletter.subject
				body = newsletter.body
				from_email = Brand.objects.first()
				from_email = from_email.public_email
				for email in newsletter.email.all():
					send_mail(subject=subject, from_email=from_email, recipient_list=[email], message=body, fail_silently=False)
			return redirect('newsletter_detail', pk=newsletter.pk)

	else:
		form = NewsletterCreationForm(instance=newsletter)

	context = {
		"form": form
	}

	return render(request, "newsletter/control_newsletter.html", context)

def newsletter_delete(request, pk):
	newsletter = get_object_or_404(Newsletter, pk=pk)

	if request.method == 'POST':
		form = NewsletterCreationForm(request.POST, instance=newsletter)

		if form.is_valid():
			newsletter.delete()
			return redirect('newsletter_list')

	else:
		form = NewsletterCreationForm(instance=newsletter)

	context = {
		'form': form
	}
	return render(request, 'newsletter/newsletter-delete.html', context)
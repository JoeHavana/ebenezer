
import os
import time
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from datetime import date, datetime
#from xhtml2pdf import pisa
from core.store.models import *
from core.site_settings.models import *
#from core.streams.choices import *
from home.models import *

year = date.today().year
today = date.today()



class SearchProducts(View):

	def get(self, *args, **kwargs):

		context = {
			'countcatgnav2': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').count(),
			'categories':ItemCategory.objects.filter(will_be_recomended=True).order_by('priority'),
		}
		return render(self.request, 'home/returned_search_results.html', context)

	def post(self, *args, **kwargs):

		if self.request.method == 'POST':
			form = self.request.POST['filter_by_products']
			search_by = (
				# TODO. Filter also by categories 
				Q(categories__category_name__icontains=form)|
				Q(title__icontains=form)|
				Q(short_description__icontains=form)|
				Q(full_description__icontains=form)
			)
			returned_search_results = Item.objects.filter(search_by).distinct()
			if returned_search_results.exists():
				context = {
					'countcatgnav2': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').count(),
					'nav2categories': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').all(),
					'items':returned_search_results,
					'items_count': returned_search_results.count(),
				}
				return render(self.request, 'home/returned_search_results.html', context)
			else:
				context = {
					'countcatgnav2': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').count(),
					'nav2categories': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').all(),
				}
				messages.info(self.request, f"Sorry, '{form}' does not match with any of our content.")
				return render(self.request, 'home/returned_search_results.html', context)

# For ItemCategory List
class AllCategories(View):

	def get(self, *args, **kwargs):

		context = {
			'countcatgnav2': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').count(),
			'nav2categories': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').all(),
			'items': Item.objects.all(),
			'categories': ItemCategory.objects.all()
		}
		return render(self.request, 'home/all_categories.html', context)


def categoryDetail(request, slug):
	context = {
		'countcatgnav2': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').count(),
		'nav2categories': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').all(),
		"items_related":Item.objects.filter(categories__slug=slug).distinct(),
		"slug":f"{slug.replace('-',' ')}",
	}
	return render(request, 'home/category_detail.html', context)

def blogCategoryDetail(request, slug):
	pass


def ItemDetail(request, slug):
	if request.user.is_authenticated:
		item = Item.objects.get(slug=slug)
		context = {
			'countcatgnav2': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').count(),
			'nav2categories': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').all(),
			'item':item,
		}
		return render(request, 'home/product-page.html', context)
	else:
		item = Item.objects.get(slug=slug)
		context = {
			'countcatgnav2': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').count(),
			'nav2categories': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').all(),
			'item':item,
		}
		return render(request, 'home/product-page.html', context)

def CartaDetail(request, slug):
	if request.user.is_authenticated:
		item = Carta.objects.get(slug=slug)
		context = {
			'countcatgnav2': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').count(),
			'nav2categories': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').all(),
			'carta':Carta.objects.all(),
			'cartas':item,
		}
		return render(request, 'home/carta.html', context)
	else:
		item = Carta.objects.get(slug=slug)
		context = {
			'countcatgnav2': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').count(),
			'nav2categories': ItemCategory.objects.filter(will_be_recomended=True).order_by('priority').all(),
			'carta':Carta.objects.all(),
			'cartas':item,
		}
		return render(request, 'home/carta.html', context)


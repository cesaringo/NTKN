from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class Home2(TemplateView):
	template_name = 'index2.html'

	

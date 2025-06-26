from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def meal_plan(request):
    return HttpResponse("Here goes the weekly mealplanner")
from django.shortcuts import render
from .models import MealPlan, MealSlot, Recipe
from .forms import MealSlotForm
from django.forms import modelformset_factory

# Create your views here.

DAYS = [choice[0] for choice in MealSlot.DaysOfWeek.choices]
MEAL_TYPES = [choice[0] for choice in MealSlot.MealType.choices]

def weekly_planner_view(request):
    meal_plan, _ = MealPlan.objects.get_or_create(user=request.user)

    for day in DAYS: 
        for meal in MEAL_TYPES:
            MealSlot.objects.get_or_create(
                meal_plan=meal_plan, day=day, meal_type=meal
            )

    slots = MealSlot.objects.filter(meal_plan=meal_plan).order_by("day", "meal_type")
    MealSlotFormSet = modelformset_factory(MealSlot, form=MealSlotForm, extra=0)

    if request.method == "POST":
        formset = MealSlotFormSet(request.POST, queryset=slots)
        if formset.is_valid():
            formset.save()
            return redirect('weekly_planner_view')
    else:
        formset = MealSlotFormSet(queryset=slots)

    
    context = {
        'formset': formset,
        'slots': slots,
        'days': MealSlot.DaysOfWeek.choices,
        'meal_types': MealSlot.MealType.choices,
    }

    return render(request, 'meal_plan/index.html' context)
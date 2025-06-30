from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to=None, max_length=100, blank=True)
    cooking_time = models.DurationField()
    serves = models.IntegerField()
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', related_name="recipes"
    )
    instructions = models.TextField()
    categories = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="recipe_tag"
    )
    notes = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.quantity} {self.ingredient.name} in {self.recipe.name}"
    

class MealPlan(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="meal_plan"
    )
    created_on = models.DateTimeField(auto_now_add=True)


class MealSlot(models.Model):

    class DaysOfWeek(models.TextChoices):
        MONDAY = "MON", ("Monday")
        TUESDAY = "TUE", ("Tuesday")
        WEDNESDAY = "WED", ("Wednesday")
        THURSDAY = "THU", ("Thursday")
        FRIDAY = "FRI", ("Friday")
        SATURDAY = "SAT", ("Saturday")
        SUNDAY = "SUN", ("Sunday")
    

    class MealType(models.TextChoices):
        BREAKFAST = "BREAKFAST", ("Breakfast")
        LUNCH = "LUNCH", ("Lunch")
        DINNER = "DINNER", ("Dinner")

    
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="meal_slots")
    day = models.CharField(max_length=9, choices=DaysOfWeek.choices)
    meal_type = models.CharField(max_length=10, choices=MealType.choices)
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("meal_plan","day", "meal_type")
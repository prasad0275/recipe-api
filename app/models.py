from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) ->str:
        return self.name
    
class RecipeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Recipe(models.Model): 
    name = models.CharField(max_length=100)
    instructions = models.TextField()
    cooking_time = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    category = models.ManyToManyField(RecipeCategory,blank=True,related_name='recipe')
    ingredient = models.ManyToManyField(Ingredient,blank=True)
    posted_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    image_url = models.ImageField(upload_to='images/',null=True,blank=True,default='images/default.jpg')

    def __str__(self) -> str:
        return self.name
    
class UserRecipe(models.Model): 
    name = models.CharField(max_length=100)
    instructions = models.TextField()
    cooking_time = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    user = models.CharField(max_length=100,blank=True,null=True)
    image_url = models.ImageField(upload_to='images/',null=True,blank=True,default='images/default.jpg')

    def __str__(self) -> str:
        return self.name
    
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class Recipe_Like(models.Model):
    pass

class Recipe_Dislike(models.Model):
    pass

class Recipe_Bookmark(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE) 

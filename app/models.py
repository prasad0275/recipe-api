from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) ->str:
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    instructions = models.TextField()
    cooking_time = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    ingredient = models.ManyToManyField(Ingredient)
    image_url = models.ImageField(upload_to='images/',null=True,blank=True,default='media/images/default.jpg')
    like = models.ManyToManyField(User,related_name="like")
    dislike = models.ManyToManyField(User,related_name="dislike") 
    bookmark = models.ManyToManyField(User,related_name="bookmark") 

    def __str__(self) -> str:
        return self.name
    
    
    
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


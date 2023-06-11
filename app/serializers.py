from rest_framework import serializers
from .models import Recipe,Ingredient
from django.contrib.auth.models import User

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','password','first_name','last_name','email']

class RecipeSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=True,read_only=True)
    like = UserSerializer(many=True)
    dislike = UserSerializer(many=True)
    bookmark = UserSerializer(many=True)
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'instructions', 'cooking_time', 'description', 'ingredient','image_url','like','dislike','bookmark']


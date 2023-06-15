from rest_framework import serializers
from .models import Recipe,Ingredient, RecipeCategory, UserRecipe
from django.contrib.auth.models import User

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class RecipeCategorySerializer1(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = ['id','name']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','password','first_name','last_name','email']

class UserSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class RecipeSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=True)
    category = RecipeCategorySerializer1(many=True)
    posted_by = UserSerializer()
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'instructions', 'cooking_time', 'description','category', 'ingredient','posted_by','image_url']

class RecipeSerializer2(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=True)
    posted_by = UserSerializer()
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'instructions', 'cooking_time', 'description', 'ingredient','posted_by','image_url']


class RecipeCategorySerializer2(serializers.ModelSerializer):
    recipe = RecipeSerializer2(many=True)
    class Meta:
        model = RecipeCategory
        fields = ['id','name','recipe']

class RecipeSerializerPost(serializers.ModelSerializer):
    # ingredient = IngredientSerializer(many=True)
    # posted_by = UserSerializer()
    # class Meta:
    #     model = Recipe
    #     fields = ['id', 'name', 'instructions', 'cooking_time', 'description', 'category', 'ingredient', 'posted_by', 'image_url']

    posted_by = UserSerializerPost()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'instructions', 'cooking_time', 'description', 'category', 'ingredient', 'posted_by', 'image_url']

    def create(self, validated_data):
        posted_by_data = validated_data.pop('posted_by', None)
        if posted_by_data:
            username = posted_by_data.get('username')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError('User does not exist.')
            validated_data['posted_by'] = user
        return super().create(validated_data)
    

class UserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecipe
        fields = ['id', 'name', 'instructions', 'cooking_time', 'description','user','image_url']
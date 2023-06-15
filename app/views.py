import io
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Recipe, Ingredient, Recipe_Bookmark, RecipeCategory, UserRecipe
from .serializers import RecipeSerializer, IngredientSerializer, UserSerializer, RecipeCategorySerializer2, UserRecipeSerializer

from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# from rest_framework.authentication import
# Create your views here.


# class get_recipe(ListCreateAPIView):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer

# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['GET','POST'])
def get_all_recipe(request):
    if request.method == 'GET':
        print(request.data)
        query = request.GET.get('q')
        if query:
            queryset = Recipe.objects.filter(name__icontains=query)
            serializer = RecipeSerializer(queryset, many=True)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data)
        queryset = Recipe.objects.all()
        serializer = RecipeSerializer(queryset, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data)
    
    # if request.method == 'POST':
    #     serializer = RecipeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data )
    #     return Response(serializer.errors)
        # data = request.data
        # name = data['name']
        # instructions = data['instructions']
        # cooking_time = data['cooking_time']
        # description = data['description']
        # category = data['category']
        # ingredients = data['ingredient']
        # posted_by = data['posted_by']['username']
        # image_url = data['image_url']

        # user = User.objects.filter(username=posted_by).first()
        # category_list = []
        # for i in category:
        #     category_list.append(RecipeCategory.objects.filter(i['name']).first())
        # ingredients_list = []
        # for i in ingredients:
        #     ingredients_list.append(Ingredient.objects.filter(i['name']).first())

        # json_data = {
        #     "name":name,
        #     "instruction":instructions,
        #     "cooking_time":cooking_time,
        #     "description":description,
        #     "category":category_list,
        #     "ingredient":ingredients_list,
        #     "posted_by":user,
        #     "image_url":image_url
        # }

        # print(json_data)
        # serializer = RecipeSerializer(data=json_data)
        # serializer.save()
        # return Response(serializer.data)

@api_view(['GET','POST'])
def post_recipe_by_user(request,user=None):
    if request.method == 'GET':
        if user is not None:
            queryset = UserRecipe.objects.filter(user=user)
            serializer = UserRecipeSerializer(queryset,many=True)
            return Response(serializer.data)
        return Response(status=400)

    if request.method == 'POST':
        data = request.data
        print(data)
        serializer = UserRecipeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=400)
    return Response(status=400)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def get_ingredients(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            queryset = Ingredient.objects.filter(name__icontains = query).order_by('name').values()
            serializer = IngredientSerializer(queryset,many=True)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data)
        
        queryset = Ingredient.objects.all().order_by('name').distinct().values()[:7]
        serializer = IngredientSerializer(queryset, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data)

@api_view(["POST"])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def get_recipe_by_ingredients(request):
    if request.method == "POST":
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        ingredients = python_data.get("data")
        print(ingredients)

        matching_list = []
        queryset = Recipe.objects.filter(ingredient__name__in=ingredients).distinct()
        for recipe in queryset:
            recipe_ingredients = recipe.ingredient.all()
            recipe_ingredient_names = set(
                ingredient.name for ingredient in recipe_ingredients
            )

            if set(ingredients).issubset(recipe_ingredient_names):
                matching_list.append(recipe)

                
            #     print("got result")
            # print(recipe_ingredient_names)
        # print(queryset)
        # print("matching list ", matching_list)
        serializer = RecipeSerializer(matching_list, many=True)
        json_data = JSONRenderer().render(serializer.data)

        return HttpResponse(json_data)
    
@api_view(["POST"])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def get_recipe_by_ingredients_loose(request):
    if request.method == "POST":
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        ingredients = python_data.get("data")
        print(ingredients)

        # matching_list = []
        queryset = Recipe.objects.filter(ingredient__name__in=ingredients).distinct()
        # for recipe in queryset:
        #     recipe_ingredients = recipe.ingredient.all()
        #     recipe_ingredient_names = set(
        #         ingredient.name for ingredient in recipe_ingredients
        #     )
        #     if set(ingredients).issubset(recipe_ingredient_names):
        #         matching_list.append(recipe)
            #     print("got result")
            # print(recipe_ingredient_names)
        # print(queryset)
        # print("matching list ", matching_list)
        serializer = RecipeSerializer(queryset, many=True)
        json_data = JSONRenderer().render(serializer.data)

        return HttpResponse(json_data)
    

@api_view(['GET','POST'])
def recipe_by_category(request):
    if request.method == 'GET':
        queryset = RecipeCategory.objects.all()
        serializer = RecipeCategorySerializer2(queryset,many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        categories = request.data['data']
        print(categories)
        queryset = Recipe.objects.filter(category__name__in=categories).distinct()
        if queryset:
            serializer = RecipeSerializer(queryset,many=True)
            return Response(serializer.data)
    return Response({'msg':'data not found'})



# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['GET','POST','PATCH','PUT','DELETE'])
def user_utilitise(request,id=None,username=None):
    if request.method == 'GET':
        # data = request.data
        if id is not None:
            queryset = User.objects.get(id=id)
            serializer = UserSerializer(queryset)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data)
        
        if username is not None:
            queryset = User.objects.get(username=username)
            serializer = UserSerializer(queryset)
            return Response(serializer.data)
        queryset = User.objects.all()
        serializer = UserSerializer(queryset,many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data)
    if request.method == 'POST':
        data = request.data
        print(data['password'])
        data['password'] = make_password(data['password'])
        serializer = UserSerializer(data=data)
        queryset = User.objects.filter(username = data['username'])
        if queryset: 
            return Response({'msg':'user already exists'},status=409)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data)
        return HttpResponse(serializer.errors)
    if request.method == 'PUT':
        data = request.data
        queryset = User.objects.get(id=data['id'])
        serializer = UserSerializer(queryset,data=data,partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors)

    if request.method == 'PATCH':
        data = request.data
        print(data)
        queryset = User.objects.get(id=data['id'])
        serializer = UserSerializer(queryset,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors)

    if request.method == 'DELETE':
        queryset = User.objects.get(id=id)
        print(queryset)
        if queryset is not None:
            queryset.delete()
            return Response({'msg':'user is successfull deleted'},status=202)
        return Response({'msg':'error'},status=500)
        

@api_view(['GET','POST','PUT'])
def recipe_bookmark(request):
    if request.method == 'POST':
        data = request.data
        user = int(data['user'])
        recipe = int(data['recipe'])

        # print(user+" "+recipe)

        user_object = User.objects.get(id=user)
        recipe_object = Recipe.objects.get(id=recipe)

        if user_object is not None and recipe_object is not None:
            print('if')
            recipe_bookmark_object = Recipe_Bookmark.objects.filter(user=user_object).filter(recipe=recipe_object)
            print(recipe_bookmark_object)
            if recipe_bookmark_object:
                recipe_bookmark_object.delete()
                return Response({'msg':'bookmark deleted'},status=200)

            new_recipe_bookmark_object = Recipe_Bookmark(user=user_object,recipe=recipe_object)
            new_recipe_bookmark_object.save()
            return Response({'msg':'bookmark save successfully'},status=200)
        
        return Response('error')

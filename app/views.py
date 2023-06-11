import io
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from .models import Recipe, Ingredient
from django.contrib.auth.models import User
from .serializers import RecipeSerializer, IngredientSerializer, UserSerializer
from rest_framework.generics import ListCreateAPIView

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

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def get_all_recipe(request):
    if request.method == 'GET':
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

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_ingredients(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            queryset = Ingredient.objects.filter(name__icontains = query).order_by('name').values()
            serializer = IngredientSerializer(queryset,many=True)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data)
        
        queryset = Ingredient.objects.all().order_by('name').values()[:5]
        serializer = IngredientSerializer(queryset, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data)

@api_view(["GET"])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def get_recipe_by_ingredients(request):
    if request.method == "GET":
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



# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['GET','POST','PATCH','PUT','DELETE'])
def user_utilitise(request,id=None):
    if request.method == 'GET':
        data = request.data
        if id is not None:
            queryset = User.objects.get(id=id)
            serializer = UserSerializer(queryset)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data)
        queryset = User.objects.all()
        serializer = UserSerializer(queryset,many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data)
    if request.method == 'POST':
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
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
def recipe_like(request):

    if request.method == 'POST':
        data = request.data
        user = data['user']
        recipe = data['recipe']

        print(user+" "+recipe)

        user_object = User.objects.get(username=user)
        recipe_object = Recipe.objects.get(name=recipe)

        if user_object is not None and recipe_object is not None:
            print('if')
            isPresent = Recipe.objects.filter(like=user_object)
            print(isPresent)
            if isPresent is not None: 
                isPresent.delete()
                return Response({'msg':'data deleted'},status=200)

            recipe_object.like.add(user_object) 
            recipe_object.save()
            return Response({'msg':'data save successfully'},status=200)
        
        return Response('error')

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
urlpatterns = [
    # operations on recipe
    # path('get_recipe',views.get_recipe.as_view()),
    path('get-all-recipe',views.get_all_recipe),
    path('get-ingredients',views.get_ingredients), 
    path('get-recipe-by-ingredients',views.get_recipe_by_ingredients),

    # like , dislike , bookmark
    path('recipe-like',views.recipe_like),

    # user
    path('user-utilitise',views.user_utilitise),
    path('user-utilitise/<int:id>',views.user_utilitise),

    # token authentication
    path('token',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh',TokenRefreshView.as_view(),name='token_refresh_token'),
    path('token/verify',TokenVerifyView.as_view(),name='verify_token'),
]


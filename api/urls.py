from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # these are the JWT tokens used to create for protected routes
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('',views.getRoutes),
    path('projects/',views.getProjects),
    path('project/<str:pk>/',views.getProject),
    path('projects/<str:pk>/vote/',views.projectVote),
    path('remove-tag/',views.removeTag),
]
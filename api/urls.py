from django.urls import path
from .views import SignupView, LoginView, LogoutView, BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('auth/register/', SignupView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
]

urlpatterns += router.urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ServicoViewSet

router = DefaultRouter()
# Rota: /api/servicos/categorias/
router.register(r'categorias', CategoriaViewSet)

# Rota: /api/servicos/servicos/
router.register(r'servicos', ServicoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
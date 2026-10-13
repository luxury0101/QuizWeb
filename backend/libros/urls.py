from rest_framework.routers import SimpleRouter

from .views import LibroViewSet

router = SimpleRouter(trailing_slash=False)
router.register("libros", LibroViewSet, basename="libro")

urlpatterns = router.urls


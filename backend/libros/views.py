from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Libro
from .serializers import LibroSerializer


@extend_schema_view(
    list=extend_schema(summary="Listar libros", responses={200: LibroSerializer(many=True)}),
    create=extend_schema(summary="Crear un libro", request=LibroSerializer, responses={201: LibroSerializer}),
    destroy=extend_schema(summary="Eliminar un libro", responses={204: None, 404: None}),
)
class LibroViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

    def destroy(self, request, *args, **kwargs):
        libro = self.get_object()
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


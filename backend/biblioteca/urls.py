from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

swagger_view = SpectacularSwaggerView.as_view(url_name="schema")

urlpatterns = [

    path("", swagger_view, name="swagger-ui"),
    path("swagger", swagger_view, name="swagger-ui-short"),
    path("swagger/", swagger_view, name="swagger-ui-slash"),
    path("docs", swagger_view, name="docs-short"),
    path("docs/", swagger_view, name="docs-slash"),
    path("admin/", admin.site.urls),
    path("api/", include("libros.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema", SpectacularAPIView.as_view(), name="schema-no-slash"),
    path("api/docs/", swagger_view, name="api-docs"),
    path("api/docs", swagger_view, name="api-docs-no-slash"),
]


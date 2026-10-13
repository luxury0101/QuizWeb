from rest_framework import serializers

from .models import Libro


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ["id", "titulo", "autor"]
        read_only_fields = ["id"]

    def validate_titulo(self, value):
        if not value.strip():
            raise serializers.ValidationError("El título es obligatorio.")
        return value.strip()

    def validate_autor(self, value):
        if not value.strip():
            raise serializers.ValidationError("El autor es obligatorio.")
        return value.strip()


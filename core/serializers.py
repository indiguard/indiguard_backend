# core/serializers.py
from rest_framework import serializers
from .models import Testimonial

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '_all_' # Include all fields from the model
        read_only_fields = ['approved', 'created_at', 'updated_at'] # User can't set these directly on creation

    def create(self, validated_data):
        # When a testimonial is created via the API, always set approved to False
        validated_data['approved'] = False
        return Testimonial.objects.create(**validated_data)

class AdminTestimonialSerializer(serializers.ModelSerializer):
    """
    Serializer for admin panel, allowing 'approved' field to be writable.
    """
    class Meta:
        model = Testimonial
        fields = '_all_'
        read_only_fields = ['created_at', 'updated_at']

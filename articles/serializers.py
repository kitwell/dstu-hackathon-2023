from rest_framework import serializers
from .models import Articles, Review





class ArticlesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ('title', 'subtitle', 'content', 'category')


class ArticlesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        exclude = ('category',)
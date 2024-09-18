from rest_framework import serializers
from blog_app.models import Article, Category
from account_app.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'parent', 'title', 'created_date', 'updated_date']


class ArticleListSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField(source='get_absolute_api_url')

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'description', 'is_active', 'categories', 'tags', 'url', 'image',
                  'created_date', 'updated_date']
        read_only_fields = ['author']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['categories'] = CategorySerializer(instance.categories, many=True).data
        rep['tags'] = CategorySerializer(instance.tags, many=True).data
        return rep


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'author', 'description', 'is_active', 'categories', 'tags', 'image',
                  'created_date', 'updated_date']
        read_only_fields = ['author']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['categories'] = CategorySerializer(instance.categories, many=True).data
        rep['tags'] = CategorySerializer(instance.tags, many=True).data
        return rep

    def create(self, validated_data):
        validated_data['author'] = User.objects.get(id=self.context.get('request').user.id)
        return super().create(validated_data)

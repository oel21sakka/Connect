from rest_framework import serializers
from .models import Post
from taggit.serializers import TaggitSerializer, TagListSerializerField
from django.utils.text import slugify

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'user':{'read_only':True},
            'slug':{'read_only':True},
            'title':{'required':True, 'min_length':3},
            'body':{'required':True},
            'publish_date':{'read_only':True},
            'publish_time':{'read_only':True},
        }
    
    def get_url(self,obj):
        return obj.get_absolute_url()
    
    def set_slug(self, validated_data):
        if 'title' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'], allow_unicode=True)
    
    def create(self, validated_data):
        self.set_slug(validated_data)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        self.set_slug(validated_data)
        return super().update(instance, validated_data)

class SinglePostSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        extra_kwargs = {
            'user':{'read_only':True},
            'slug':{'read_only':True},
            'title':{'required':False, 'min_length':3},
            'body':{'required':False},
            'publish_date':{'read_only':True},
            'publish_time':{'read_only':True},
            'tags':{'required':False},
        }
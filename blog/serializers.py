from datetime import date
from rest_framework import serializers
from .models import Post, Comment
from taggit.serializers import TaggitSerializer, TagListSerializerField
from django.utils.text import slugify
from django.db.models import Count,Q
from django.core.cache import cache

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'user':{'read_only':True},
            'publish_date':{'read_only':True},
            'update_date':{'read_only':True},
            'body':{'required':True},
            'post':{'required':True},
        }

class SingleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'user':{'read_only':True},
            'publish_date':{'read_only':True},
            'update_date':{'read_only':True},
            'body':{'required':True},
            'post':{'read_only':True},
        }

class BasePostSerializer(TaggitSerializer, serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    tags = TagListSerializerField(required=False)
    views_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    
    def get_url(self,obj):
        return obj.get_absolute_url()
    
    def get_views_count(self,obj):
        return cache.get(obj.get_views_cach_key(),0)
    
    def get_likes_count(self,obj):
        return obj.users_like.count()
    
    def set_slug(self, validated_data, id=None):
        if 'title' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'], allow_unicode=True)
        # Check for uniqueness of slug and publish_date
        if Post.objects.filter(Q(publish_date=date.today()) & Q(slug=validated_data['slug'])).exclude(id=id).exists():
            raise serializers.ValidationError('A post with the same title and publish date already exists.')
    

class PostSerializer(BasePostSerializer):

    class Meta:
        model = Post
        exclude = ['users_like']
        extra_kwargs = {
            'user':{'read_only':True},
            'slug':{'read_only':True},
            'title':{'required':True, 'min_length':3},
            'body':{'required':True},
            'publish_date':{'read_only':True},
        }

    def create(self, validated_data):
        self.set_slug(validated_data)
        return super().create(validated_data)


class SinglePostSerializer(BasePostSerializer):
    similar_posts = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta():
        model = Post
        exclude=['users_like']
        extra_kwargs = {
            'user':{'read_only':True},
            'slug':{'read_only':True},
            'title':{'required':False, 'min_length':3},
            'body':{'required':False},
            'publish_date':{'read_only':True},
            'tags':{'required':False},
            'similar_posts':{'read_only':True},
            'comments':{'read_only':True},
        }
    
        
    def update(self, instance, validated_data):
        self.set_slug(validated_data,instance.id)
        return super().update(instance, validated_data)
    
    def get_similar_posts(self, obj):
        similar_posts = Post.objects.filter(tags__in=obj.tags.all()).exclude(id=obj.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish_date')[:3]
        return PostSerializer(similar_posts, many=True).data
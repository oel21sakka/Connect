from datetime import date
from rest_framework import serializers
from .models import Post, Comment
from taggit.serializers import TaggitSerializer, TagListSerializerField
from django.utils.text import slugify
from django.db.models import Count,Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

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
        }
    
    def get_url(self,obj):
        return obj.get_absolute_url()
    
    def set_slug(self, validated_data, id=None):
        if 'title' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'], allow_unicode=True)
        # Check for uniqueness of slug and publish_date
        if Post.objects.filter(Q(publish_date=date.today()) & Q(slug=validated_data['slug'])).exclude(id=id).exists():
            raise serializers.ValidationError('A post with the same title and publish date already exists.')

    
    def create(self, validated_data):
        self.set_slug(validated_data)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        self.set_slug(validated_data,instance.id)
        return super().update(instance, validated_data)

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

class SinglePostSerializer(PostSerializer):
    similar_posts = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta(PostSerializer.Meta):
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
    
    def get_similar_posts(self, obj):
        similar_posts = Post.objects.filter(tags__in=obj.tags.all()).exclude(id=obj.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish_date')[:3]
        return PostSerializer(similar_posts, many=True).data

class SearchSerializer(serializers.Serializer):
    query = serializers.CharField()
    
    def search(self):
        search_vector = SearchVector('title', weight='A', config='simple') + SearchVector('body', weight='B', config='simple')
        search_query = SearchQuery(self.validated_data['query'], config='simple')
        
        results = (
            Post.objects
            .annotate(search=search_vector, rank=SearchRank(search_vector, search_query))
            .filter(search=search_query)
            .order_by('-rank')
        )
        
        return PostSerializer(results, many=True).data
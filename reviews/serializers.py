from django.urls import reverse_lazy
from rest_framework import serializers

from .models import Comment
from accounts.models import User


class CommentSerializer(serializers.ModelSerializer):
    update_url = serializers.SerializerMethodField(read_only=True)
    delete_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'content',
            'update_url',
            'delete_url',
        )

    def get_update_url(self, obj):
        if not hasattr(obj, 'id'):
            return None
        return reverse_lazy('reviews:comment_update', kwargs={'comment_pk': obj.pk})
    
    
    def get_delete_url(self, obj):
        if not hasattr(obj, 'id'):
            return None
        return reverse_lazy('reviews:comment_delete', kwargs={'comment_pk': obj.pk})


    def create(self, validated_data):
        review, user = self.context.get('review'), self.context.get('user')
        return Comment.objects.create(review=review, user=user, **validated_data)
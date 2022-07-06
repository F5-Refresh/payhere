from rest_framework import serializers
from account_books.models import AccountCategory
from users.models import User

class AcoountCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountCategory
        fields = ['id', 'user', 'category_name', 'created_at', 'modified_at']

        ordering = ['category_name']

class AcoountCategoryPostSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        user_id = validated_data.get('user').id
        user = User.objects.get(id=user_id)
        category_name = validated_data.get('category_name')
        return AccountCategory.objects.create(user=user, category_name=category_name)

    class Meta:
        model = AccountCategory
        fields = ['category_name', 'user']
        
class AcoountCategoryPutSerializer(serializers.ModelSerializer):
    
    def update(self, instance, validated_data):
        instance.category_name = validated_data.get('category_name')
        instance.save()
        return instance
        
    class Meta:
        model = AccountCategory
        fields = ['category_name']
        ordering = ['category_name']

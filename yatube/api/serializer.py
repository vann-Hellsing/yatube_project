from rest_framework import serializers

from posts.models import Post, Group, Tag, TagPost, User


class UserSerializer(serializers.ModelSerializer):
    # posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:

        fields = ('id', 'posts', 'username', 'first_name', 'last_name',  'email')
        ref_name = 'ReadOnlyUser'
        model = User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    publication_date = serializers.DateTimeField(source='pub_date', read_only=True)
    tag = TagSerializer(many=True, required=False)
    character_quantity = serializers.SerializerMethodField()
    group = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field='slug',
        required=False
    )

    class Meta:

        fields = ('text', 'author', 'image', 'publication_date', 'group', 'tag', 'character_quantity')
        read_only_fields = ('author',)
        model = Post

    def get_character_quantity(self, obj):
        return len(obj.text)

    def create(self, validated_data):
        # Если тэг не содержится в данных, создаем новый пост
        if 'tag' not in self.initial_data:
            post = Post.objects.create(**validated_data)
            return post

        tags = validated_data.pop('tag')
        post = Post.objects.create(**validated_data)
        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(
                **tag
            )
            TagPost.objects.create(
                tag=current_tag, post=post
            )
            return post

from rest_framework import serializers
from posts.models import Post
from django_comments.models import Comment
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(style={'input_type':'password'}, write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		new_user = User(username=username)
		new_user.set_password(password)
		new_user.save()
		return validated_data

class UserLoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField(style={'input_type':'password'}, write_only=True)
	token = serializers.CharField(allow_blank=True, read_only=True)

	def validate(self, data):
		user_obj = None

		username = data.get('username')
		password = data.get('password')

		user = User.objects.filter(username=username)
		if user.exists():
			user_obj = user.first()
			if not user_obj.check_password(password):
				raise serializers.ValidationError("Wrong username/password combination! Noob!")
		else:
			raise serializers.ValidationError("This username does not exist! Go away!")

		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

		payload = jwt_payload_handler(user_obj)
		token = jwt_encode_handler(payload)
		data["token"] = token
		return data


class UserDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']

class PostListSerializer(serializers.ModelSerializer):
	detail = serializers.HyperlinkedIdentityField(
		view_name="api:detail",
		lookup_field="slug",
		lookup_url_kwarg = "post_slug"
		)
	class Meta:
		model = Post
		fields = ['id','title', 'publish', 'detail']

class PostDetailSerializer(serializers.ModelSerializer):
	author = UserDetailSerializer()
	comments = serializers.SerializerMethodField()
	class Meta:
		model = Post
		fields = ['id','title', 'author', 'slug', 'content', 'publish', 'draft', 'comments']

	def get_comments(self, obj):
		comment_queryset = Comment.objects.filter(object_pk=obj.id)
		return CommentListSerializer(comment_queryset, many=True).data

class PostCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['title', 'content', 'draft', 'publish']


class CommentListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['user', 'comment', 'object_pk']


class CommentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['comment', 'object_pk']
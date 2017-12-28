from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

# class SnippetSerializer(serializers.Serializer):
# 	#begin defining what gets included in serialization
# 	id = serializers.IntegerField(read_only=True)
# 	title = serializers.CharField(required=False, allow_blank=True, max_length=100)
# 	code = serializers.CharField(style={'base_template':'textarea.html'}) #field flag similar to widgets.TextArea in dj.Forms
# 	linenos = serializers.BooleanField(required=False)
# 	language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python3')
# 	style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
# 	#end defining what gets included in serialization

# 	#create and return new Snippet instance, given the vlaidated data
# 	def create(self, validated_data):
# 		return Snippet.objects.create(**validated_data)

# 	#update and return an existing Snippet instance, given the validated data
# 	def update(self, instance, validated_data):
# 		instance.title = validated_data.get('title', instance.title)
# 		instance.code = validated_data.get('code', instance.code)
# 		instance.linenos = validated_data.get('linenos', instance.linenos)
# 		instance.language = validated_data.get('language', instance.language)
# 		instance.style = validated_data.get('style', instance.style)
# 		instance.save()
# 		return instance

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username') #snippet onwer
	#^^ could also use CharField(read_only=True)
	highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

	class Meta:
		model = Snippet
		fields = ('url', 'id', 'highlight', 'title', 'code', 'linenos', 'language', 'style', 'owner')



class UserSerializer(serializers.HyperlinkedModelSerializer):
#	snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
	snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

	class Meta:
		model = User
		fields = ('url', 'id', 'username', 'snippets')

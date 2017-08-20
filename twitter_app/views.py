from allauth.socialaccount.admin import SocialApp
from requests_oauthlib import OAuth1
from urllib.parse import quote
import requests
from django.http import JsonResponse

def twitter_test(request):
	person = request.user
	twitter_account = person.socialaccount_set.get(user=person.id)
	
	token_object = twitter_account.socialtoken_set.get(account=twitter_account.id)
	token = token_object.token
	token_secret = token_object.token_secret

	social_app = SocialApp.objects.get(provider=twitter_account.provider)
	client_id = social_app.client_id
	client_secret = social_app.secret

	x = OAuth1(client_id, client_secret, token, token_secret)

	search_stuff= quote("from:m1shaal")
	url = 'https://api.twitter.com/1.1/search/tweets.json?q=%s&result_type=recent'%(search_stuff)

	response = requests.get(url, auth=x)

	return JsonResponse(response.json(), safe=False)
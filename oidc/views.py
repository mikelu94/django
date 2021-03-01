from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from authlib.integrations.django_client import OAuth

oauth = OAuth()
oauth.register(
    name='okta',
    authorization_endpoint='https://dev-4359056.okta.com/oauth2/default/v1/authorize',
    jwks_uri='https://dev-4359056.okta.com/oauth2/default/v1/keys',
    token_endpoint='https://dev-4359056.okta.com/oauth2/default/v1/token',
    # server_metadata_url='https://dev-4359056.okta.com/oauth2/default/.well-known/oauth-authorization-server',  # alternative to 3 parameters above
    client_kwargs = { 'scope': 'openid profile email' }
)

# Create your views here.
def authn(request, user=None):
    redirect_uri = request.build_absolute_uri(reverse(user_data))
    state = request.GET.get('next')  # typically encrypted
    return oauth.okta.authorize_redirect(request, redirect_uri, state=state) 

def user_data(request):
    token = oauth.okta.authorize_access_token(request)
    user_data = oauth.okta.parse_id_token(request, token)
    user, _ = User.objects.get_or_create(
        username=user_data.get('preferred_username'),
        first_name=user_data.get('name').split(' ')[0],
        last_name=user_data.get('name').split(' ')[1],
        email=user_data.get('email'),
        is_staff=True,
        is_superuser=True,
    )
    login(request, user)

    state = request.GET.get('state')
    return redirect(state)

def user_logout(request):
    logout(request)
    return HttpResponse('You have been logged out.')

@login_required
def root(request):
    return HttpResponse(f'Hi {request.user.email}, You are logged in.')
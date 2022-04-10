import logging

from authlib.integrations.django_client import OAuth
from authlib.integrations.requests_client import OAuth2Auth
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
import requests


logger = logging.getLogger(__name__)

oauth = OAuth()
oauth.register(
    name='okta',
    authorization_endpoint=f'{settings.OKTA_DOMAIN}/oauth2/default/v1/authorize',
    jwks_uri=f'{settings.OKTA_DOMAIN}/oauth2/default/v1/keys',
    token_endpoint=f'{settings.OKTA_DOMAIN}/oauth2/default/v1/token',
    # server_metadata_url=f'{settings.OKTA_DOMAIN}/oauth2/default/.well-known/openid-configuration',  # alternative to 3 parameters above
    client_kwargs = { 'scope': 'openid profile email' }
)


# Create your views here.
def authn(request, user=None):
    redirect_uri = request.build_absolute_uri(reverse(authn_redirect))
    state = request.GET.get('next')  # typically encrypted
    logger.info('Initiating SSO')
    return oauth.okta.authorize_redirect(request, redirect_uri, state=state) 


def authn_redirect(request):
    logging.info('SSO callback invoked')
    access_token = oauth.okta.authorize_access_token(request)
    userinfo = access_token.get('userinfo')

    resp = requests.get(f'{settings.OKTA_DOMAIN}/oauth2/default/v1/userinfo', auth=OAuth2Auth(access_token))
    additional_userinfo = resp.json()

    user, _ = User.objects.get_or_create(
        username=userinfo.get('preferred_username'),
        first_name=additional_userinfo.get('given_name'),
        last_name=additional_userinfo.get('family_name'),
        email=userinfo.get('email'),
        is_staff=True,
        is_superuser=True,
    )
    login(request, user)
    logging.info('Logging in %s', user)

    state = request.GET.get('state')
    return redirect(state)


def user_logout(request):
    logging.info('Logging out %s', request.user)
    logout(request)
    return HttpResponse('You have been logged out.')


@login_required
def index(request):
    logging.info('%s accessed oidc index', request.user.email)
    return HttpResponse(f'Hi {request.user.email}, You are logged in.')

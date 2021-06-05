import logging

from authlib.integrations.django_client import OAuth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


logger = logging.getLogger(__name__)

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
    redirect_uri = request.build_absolute_uri(reverse(authn_redirect))
    state = request.GET.get('next')  # typically encrypted
    logger.info("Initiating SSO")
    return oauth.okta.authorize_redirect(request, redirect_uri, state=state) 


def authn_redirect(request):
    logging.info('SSO callback invoked')
    token = oauth.okta.authorize_access_token(request)
    user_info = oauth.okta.parse_id_token(request, token)
    user, _ = User.objects.get_or_create(
        username=user_info.get('preferred_username'),
        first_name=user_info.get('name').split(' ')[0],
        last_name=user_info.get('name').split(' ')[1],
        email=user_info.get('email'),
        is_staff=True,
        is_superuser=True,
    )
    login(request, user)
    logging.info(f'Logging in f{user}')

    state = request.GET.get('state')
    return redirect(state)


def user_logout(request):
    logging.info(f'Logging out f{request.user}')
    logout(request)
    return HttpResponse('You have been logged out.')


@login_required
def index(request):
    logging.info(f'{request.user.email} accessed oidc index')
    return HttpResponse(f'Hi {request.user.email}, You are logged in.')
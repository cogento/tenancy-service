import json
from datetime import datetime, timedelta

import requests
from cogento_core.logging import logger, Logger
from cogento_core.settings import AppSettings
from cogento_core.utils import register_global_object, GlobalObject


@register_global_object(dependencies=[AppSettings, Logger])
class Auth0Provider(GlobalObject):
    """
    Auth0Provider is a class that provides methods to interact with the Auth0 Management API
    """

    def __init__(self, app_settings: AppSettings):
        super().__init__()
        self._client_id = app_settings.auth0_client_id
        self._platform_client_id = app_settings.auth0_platform_client_id
        self._client_secret = app_settings.auth0_client_secret
        self._auth0_domain = app_settings.auth0_domain
        self._access_token = None
        self._access_token_expiration = None

    def setup(self) -> None:
        logger.info("Setting up Auth0Provider...")
        self.get_access_token()

    def _get_access_token(self):
        """
        Get an access token from Auth0 and update expiration time
        :return: access token
        """
        url = f"https://{self._auth0_domain}/oauth/token"
        headers = {
            "content-type": "application/json"
        }
        data = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "audience": f"https://{self._auth0_domain}/api/v2/",
            "grant_type": "client_credentials"
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()

    def get_access_token(self):
        """
        Get an access token from Auth0 if it is expired or does not exist, otherwise return the existing token.
        :return: access token
        """
        if self._access_token is None or datetime.now() > self._access_token_expiration:
            logger.info("Requesting new access token from Auth0 as the current one is expired or does not exist")
            access_token_response = self._get_access_token()
            self._access_token = access_token_response["access_token"]
            self._access_token_expiration = datetime.now() + timedelta(seconds=access_token_response["expires_in"])
            logger.info(f"New access token expires at {self._access_token_expiration}")
        return self._access_token

    def _get_headers(self):
        return {
            "content-type": "application/json",
            "authorization": f"Bearer {self.get_access_token()}"
        }

    def _get_url(self, path: str):
        return f"https://{self._auth0_domain}/api/v2/{path}"

    def _validate_response(self, response):
        if not response.ok:
            logger.error(f"Error response from Auth0: {response.text}")
        response.raise_for_status()

    def get_organization_by_name(self, organization_name: str):
        """
        Get an organization by name from Auth0
        :param organization_name: organization name
        :return: organization
        """
        logger.info(f"Getting organization {organization_name}")
        url = self._get_url(f"organizations/name/{organization_name}")
        response = requests.get(url, headers=self._get_headers())
        self._validate_response(response)
        return response.json()

    def delete_organization(self, organization_name: str):
        """
        Delete an organization from Auth0
        :param organization_name: organization name
        """
        logger.warning(f"Deleting organization {organization_name}")
        org_id = self.get_organization_by_name(organization_name)["id"]
        delete_url = self._get_url(f"organizations/{org_id}")
        response = requests.delete(delete_url, headers=self._get_headers())
        self._validate_response(response)
        logger.info(f"Deleted organization {organization_name}")

    def create_organization(self, organization_name: str, organization_display_name: str):
        """
        Create an organization in Auth0
        :param organization_name: organization name
        :param organization_display_name: organization display name
        :return: organization id
        """
        logger.info(f"Creating organization {organization_name}")
        url = self._get_url("organizations")

        data = {
            "name": organization_name,
            "display_name": organization_display_name
        }
        response = requests.post(url, headers=self._get_headers(), data=json.dumps(data))
        self._validate_response(response)
        logger.info(f"Created organization {organization_name}")
        return response.json()['id']

    def invite_user(self, organization_id: str, organization_name: str, email: str):
        """
        Invite a user to an organization in Auth0
        :param organization_id: organization id
        :param organization_name: organization name
        :param email: user email
        :return: response from Auth0
        """
        logger.info(f"Inviting user {email} to organization {organization_name}")
        url = f"https://{self._auth0_domain}/api/v2/organizations/{organization_id}/invitations"
        data = {
            "inviter": {
                "name": organization_name
            },
            "invitee": {
                "email": email
            },
            "client_id": self._platform_client_id,
            "send_invitation_email": True
        }
        response = requests.post(url, headers=self._get_headers(), data=json.dumps(data))
        self._validate_response(response)
        logger.info(f"Invited user {email} to organization {organization_name}")
        return response.json()

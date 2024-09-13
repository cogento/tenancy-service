from cogento_core.settings import AppSettings
from cogento_core.utils import register_global_object

from cogento_core.utils import GlobalObjectProxy
import stripe


@register_global_object(dependencies=[AppSettings])
class StripeService(GlobalObjectProxy):
    def __init__(self, app_settings: AppSettings):
        super().__init__()
        self.settings = app_settings
        self._api_key = app_settings.stripe_api_key

    def _setup_proxy_impl(self) -> None:
        self._instance = stripe.StripeClient(
            api_key=self._api_key,
            max_network_retries=self.settings.get('stripe_max_network_retries', 2)
        )

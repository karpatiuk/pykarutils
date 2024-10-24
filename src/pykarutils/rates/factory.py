from typing import Union

from .providers.bnm import BnmProvider
from .providers.fixer import FixerProvider

class RateFactory:
    """Factory class for rate providers."""

    @staticmethod
    def get_provider(name: str, api_key: str = None) -> Union[BnmProvider,FixerProvider, None]:
        """Get a rate provider by name."""
        match name:
            case BnmProvider.PROVIDER_NAME:
                return BnmProvider()
            case FixerProvider.PROVIDER_NAME:
                return FixerProvider(api_key)
            case _:
                return None
from typing import Union

from .providers.bnm import BnmProvider

class RateFactory:
    """Factory class for rate providers."""

    @staticmethod
    def get_provider(name: str) -> Union[BnmProvider, None]:
        """Get a rate provider by name."""
        if name == BnmProvider.PROVIDER_NAME:
            return BnmProvider()
        return None
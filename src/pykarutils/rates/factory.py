from .providers.bnm import BnmProvider

class RateFactory:
    """Factory class for rate providers."""

    @staticmethod
    def get_provider(name):
        """Get a rate provider by name."""
        if name == 'bnm':
            return BnmProvider()
        return None
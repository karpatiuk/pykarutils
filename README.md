# PyKarUtils

`PyKarUtils` is a Python utility package that simplifies common tasks with a set of helper functions, factory patterns,
and result handling utilities. This package is modular and consists of multiple components designed for different
purposes, making it highly adaptable to various Python projects.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

You can install the package using `pip`:

```bash
pip install pykarutils
```

Alternatively, if you're installing from the source:

```bash
git clone https://github.com/karpatiuk/pykarutils.git
cd pykarutils
python setup.py install
```

## Usage

Here is a simple example of how to use some of the utility functions from PyKarUtils:

### BNM Rate Provider
```python
from pykarutils import BnmProvider, RateFactory

# Initialize the provider
provider = RateFactory.get_provider(BnmProvider.PROVIDER_NAME)

# Get rates for a specific date
rates_result = provider.get_rates('02.10.2024')

# Print the rates
for code, rate in rates_result.rates.items():
    print(f"{rate.name} ({rate.code}): {rate.rate} {rate.base_currency}")
```

### Fixer Rate Provider
```python
from pykarutils import FixerProvider, RateFactory

# Initialize the provider
provider = RateFactory.get_provider(FixerProvider.PROVIDER_NAME,'your_api_key')

# Get rates for a specific date
rates_result = provider.get_rates('2024-10-25')

# Print the rates
for code, rate in rates_result.rates.items():
    print(f"{rate.name} ({rate.code}): {rate.rate} {rate.base_currency}")
```

## Contributing

We welcome contributions to enhance the functionality of PyKarUtils. Feel free to submit issues or pull requests to the
repository.

1. Fork the repository.
2. Create your feature branch: ```git checkout -b feature/YourFeature.```
3. Commit your changes: ```git commit -m 'Add some feature'.```
4. Push to the branch: ```git push origin feature/YourFeature.```
5. Open a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
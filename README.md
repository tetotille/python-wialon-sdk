# 🚀 Wialon SDK

[![Lint and Type Check](https://github.com/tetotille/python-wialon-sdk/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/tetotille/python-wialon-sdk/actions/workflows/python-package.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c7748bd584ca463d82fd94154b8d7716)](https://app.codacy.com/gh/tetotille/python-wialon-sdk/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

## 📋 Index

- [🚀 Wialon SDK](#-wialon-sdk)
  - [📋 Index](#-index)
  - [🚀 Description](#-description)
  - [✨ Characteristics](#-characteristics)
  - [🛠 Installation](#-installation)
    - [Previous requirements](#previous-requirements)
  - [📚 Use](#-use)
  - [📄 Documentation](#-documentation)
  - [🔍 Examples](#-examples)
  - [🤝 Contributions](#-contributions)
  - [🛣 Roadmap](#-roadmap)
  - [📄 License](#-license)
  - [💬 Acknowledgments](#-acknowledgments)
  - [📫 Contact](#-contact)

## 🚀 Description

This is an unofficial SDK for Wialon's API, developed to simplify integration with the Wialon vehicle and fleet management system. This SDK allows access to various functionalities of the Wialon system through a simple and powerful Python interface.

## ✨ Characteristics

- 📡 Authentication and session management
- 📊 Real-time data access and historical reports
- 🚗 Management of units, drivers, and geofences
- 🔄 Asynchronous functions for improved performance
- 🔧 Python 3.8+ compatibility

## 🛠 Installation

You can install the SDK using pip:

```bash
# Clone the repository
git clone https://github.com/tetotille/wialon-sdk.git

# Navigate to the project directory
cd wialon-sdk

# Install the package
pip install .
```

### Previous requirements

- Python 3.8 or higher
- An active account in Wialon Hosting
- Wialon API Key

## 📚 Use

Below is an example of how to start using the SDK:

```python
from wialon import Wialon

# Initialize the connection with the API key
client = Wialon(api_url="https://hst-api.wialon.com/wialon/ajax.html", api_key="YOUR_API_KEY")

# Authenticate with the API
client.auth.login("YOUR_API_KEY")

# Obtain the list of units
units = client.request("core/search_items", {"spec": {"itemsType": "avl_unit", "propName": "sys_name", "propValueMask": "*", "sortType": "sys_name"}, "force": 1, "flags": 1, "from": 0, "to": 0})
for unit in units['items']:
    print(f"Unit: {unit['nm']}, ID: {unit['id']}")

# Obtain historical data
history = client.messages.load_interval(item_id=12345, time_from=datetime(2023, 1, 1), time_to=datetime(2023, 1, 2))
print(history)
```

## 📄 Documentation

Consult the complete documentation for more details about all available features.

## 🔍 Examples

Some additional examples to perform common tasks:

1. Authentication and session management
2. Obtaining real-time locations
3. Generation of activity reports

Check the `examples` folder for more examples.

## 🤝 Contributions

Contributions are welcome! If you want to contribute, follow these steps:

1. Fork the project.
2. Create a branch for your feature (`git checkout -b feature/new-functionality`).
3. Commit your changes (`git commit -m 'Add new functionality'`).
4. Push your changes (`git push origin feature/new-functionality`).
5. Open a Pull Request.

Check the `CONTRIBUTING.md` file for more details.

## 🛣 Roadmap

- [x] Basic authentication and session management
- [ ] Initial support for unit management
- [ ] Fetching real-time data
- [ ] Basic historical data retrieval
- [ ] Documentation and examples for initial features
- [ ] Community feedback and initial improvements

## 📄 License

This project is under the **[MIT License](LICENSE)**. Check the LICENSE file for more details.

Note: You can use, modify, and distribute this software freely, provided you maintain attribution to the original author.

## 💬 Acknowledgments

To all developers and the community for their support and contributions to this project.

## 📫 Contact

If you have questions or suggestions, do not hesitate to open an issue.

# TRON Address Generator

A web application that generates TRON addresses and verifies the relationship between private keys and TRON addresses. Built with Python Flask and JavaScript.

## Features

- Generate new TRON addresses
- Generate corresponding private and public keys
- Verify TRON addresses against private keys
- Copy-to-clipboard functionality for all generated values

## Prerequisites

- Python 3.x
- Flask
- Other dependencies (listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tron-address-generator.git
cd tron-address-generator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:8000
```

3. Click the "Generate New Address" button to create a new TRON address with its corresponding keys.

## API Endpoints

### Generate New Address
- **URL:** `/generate`
- **Method:** `POST`
- **Response:** JSON containing private key, public key, and TRON address

### Verify Address
- **URL:** `/verify/<private_key>/<tron_address>`
- **Method:** `GET`
- **Response:** JSON indicating if the private key matches the TRON address

## Security Considerations

- Never share your private key
- Generate addresses in a secure environment
- Use HTTPS in production

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
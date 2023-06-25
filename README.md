# dotenv-to-sealed-secrets

This project provides a utility script to convert `.env` files to Kubernetes Sealed Secrets. It's useful for developers who want to maintain Kubernetes Secrets in a `.env` file format during development, and then convert them to Sealed Secrets for use in a Kubernetes cluster.

## Requirements

- Python 3.7 or later
- [`kubeseal`](https://github.com/bitnami-labs/sealed-secrets#installation)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/dokdo2013/dotenv-to-sealed-secrets.git
cd dotenv-to-sealed-secrets
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

To convert a `.env` file to Sealed Secrets, run the script with the path to the `.env` file:

```bash
python3 script.py path/to/your/.env
```

The script supports the following options:

- `--name`: Set the name of the Secret. Default is 'mysecret'.
- `--controller-name`: Set the controller name for Kubeseal. Default is 'sealed-secrets'.
- `--controller-namespace`: Set the controller namespace for Kubeseal. Default is 'kube-system'.
- `--print-none`: Do not print the sealed secret to stdout. If not set, the sealed secret is printed.
- `--output`: Keep the generated secret.yaml and sealed-secret.yaml files. If not set, the files are removed.

For more details on these options, run:

```bash
python3 script.py --help
```

You can also set up an alias for convenience. For example, in your `.zshrc` or `.bashrc`, you can add the following line:

```bash
alias envto='python3 /path/to/script.py'
```

Then, you can simply use `envto path/to/your/.env` to run the script.

Remember to reload your shell or run `source ~/.zshrc` (or `source ~/.bashrc`) for the changes to take effect.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

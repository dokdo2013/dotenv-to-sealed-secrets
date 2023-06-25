import argparse
import base64
import os
import shlex
import subprocess
import sys
import yaml


def env_to_secret(env_path, output_path, name='mysecret'):
    data = {}

    with open(env_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            key = key.strip()

            value = shlex.split(value)[0]

            data[key] = base64.b64encode(value.encode()).decode()

    secret = {
        'apiVersion': 'v1',
        'kind': 'Secret',
        'metadata': {
            'name': name,
        },
        'type': 'Opaque',
        'data': data,
    }

    with open(output_path, 'w') as file:
        yaml.dump(secret, file)

    return secret


def seal_secret(input_path, controller_name='sealed-secrets', controller_namespace='kube-system', print_none=False):
    command = f"kubeseal --format=yaml --controller-name {controller_name} --controller-namespace {controller_namespace} < {input_path}"

    if print_none:
        command += " > sealed-secret.yaml"
    else:
        command += " | tee sealed-secret.yaml"

    subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert .env to sealed secrets")
    parser.add_argument('source', nargs='?', default='.env',
                        help="Path to the .env file. Default is '.env' in the current directory.")
    parser.add_argument('--name', default='mysecret',
                        help="Name of the Secret. Default is 'mysecret'.")
    parser.add_argument('--controller-name', default='sealed-secrets',
                        help="Controller name for Kubeseal. Default is 'sealed-secrets'.")
    parser.add_argument('--controller-namespace', default='kube-system',
                        help="Controller namespace for Kubeseal. Default is 'kube-system'.")
    parser.add_argument('--print-none', action='store_true',
                        help="Do not print the sealed secret to stdout. If not set, the sealed secret is printed.")
    parser.add_argument('--output', action='store_true',
                        help="Keep the generated secret.yaml and sealed-secret.yaml files. If not set, the files are removed.")

    args = parser.parse_args()

    secret = env_to_secret(args.source, 'secret.yaml', args.name)
    seal_secret('secret.yaml', args.controller_name,
                args.controller_namespace, args.print_none)

    if not args.output:
        os.remove('secret.yaml')
        if args.print_none or not args.output:
            os.remove('sealed-secret.yaml')

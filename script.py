import argparse
import base64
import os
import shlex
import subprocess
import sys
import yaml


def env_to_secret(env_path, output_path, name='mysecret', namespace='default'):
    data = {}

    try:
        with open(env_path, 'r') as file:
            for line in file:
                line = line.strip()

                # skip empty lines
                if line == "":
                    continue

                # skip comments
                if line.startswith("#"):
                    continue

                key, value = line.split('=', 1)
                key = key.strip()

                values = shlex.split(value)

                # when the empty value provided, the 0 index is empty
                value = values[0] if values else ""

                data[key] = base64.b64encode(value.encode()).decode()
    except FileNotFoundError:
        print("[Error] Please provide a valid path to the .env file.")
        sys.exit(1)
    except Exception as e:
        print(f"[Error] {e}")
        sys.exit(1)

    secret = {
        'apiVersion': 'v1',
        'kind': 'Secret',
        'metadata': {
            'name': name,
            'namespace': namespace,
        },
        'type': 'Opaque',
        'data': data,
    }

    with open(output_path, 'w') as file:
        yaml.dump(secret, file)

    return secret


def seal_secret(input_path, controller_name='sealed-secrets', controller_namespace='kube-system', print_none=False, scope='cluster-wide'):
    command = f"kubeseal --scope {scope} --format=yaml --controller-name {controller_name} --controller-namespace {controller_namespace} < {input_path}"

    if print_none:
        command += " > /tmp/sealed-secret.yaml"
    else:
        command += " | tee /tmp/sealed-secret.yaml"

    subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert .env to sealed secrets")
    parser.add_argument('--source', default='.env',
                        help="Path to the .env file. Default is '.env' in the current directory.")
    parser.add_argument('--name', default='mysecret',
                        help="Name of the Secret. Default is 'mysecret'.")
    parser.add_argument('--namespace', default='default',
                        help="Namespace of the Secret. Default is 'default'.")
    parser.add_argument('--controller-name', default='sealed-secrets',
                        help="Controller name for Kubeseal. Default is 'sealed-secrets'.")
    parser.add_argument('--controller-namespace', default='kube-system',
                        help="Controller namespace for Kubeseal. Default is 'kube-system'.")
    parser.add_argument('--scope', default='cluster-wide',
                        help="Scope of the sealed secret. If not set, the scope is 'cluster-wide'.")
    parser.add_argument('--print-none', action='store_true',
                        help="Do not print the sealed secret to stdout. If not set, the sealed secret is printed.")
    parser.add_argument('--output', action='store_true',
                        help="Keep the generated secret.yaml and sealed-secret.yaml files. If not set, the files are removed.")

    args = parser.parse_args()

    secret = env_to_secret(args.source, '/tmp/secret.yaml',
                           args.name, args.namespace)
    seal_secret('/tmp/secret.yaml', args.controller_name,
                args.controller_namespace, args.print_none, args.scope)

    if args.output:
        os.system(f"cp /tmp/secret.yaml ./secret.yaml")
        os.system(f"cp /tmp/sealed-secret.yaml ./sealed-secret.yaml")

    os.remove('/tmp/secret.yaml')
    os.remove('/tmp/sealed-secret.yaml')

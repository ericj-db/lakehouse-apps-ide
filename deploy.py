import requests
import argparse
import uuid

parser = argparse.ArgumentParser()
parser.add_argument('--dry_run', default=True)
parser.add_argument('--host', help='Databricks host to deploy app to', default='dbc-e2ec9f4b-f2a7.dev.databricks.com')
parser.add_argument('--pat', help='Personal Access Token to use for deployment', default='dapidec49111d80a219f54f7a454a7949ce0')
# Can possibly get this directly from github workflow
parser.add_argument('--access_key', help='Github access key to pass to Harbor', default='ericj-db')
parser.add_argument('--access_secret', help='Github access secret to pass to Harbor', default='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')

args = parser.parse_args()

if args.dry_run:
    exit(0)

app_name = uuid.uuid4().hex
url = f'https://{args.host}/api/2.0/preview/apps/deployments'
headers = {'Authorization': f'Bearer {args.pat}'}
body = {
  'manifest': {
    'version': '1',
    'name': app_name,
    'description': 'Amuseable Avocado',
    'ingress': {
        'endpoints': [
            {
                'port_name': 'app-http',
                'visibility': 'EXTERNAL'
            }
        ]
    },
    'registry': {
      'url': 'https://ghcr.io',
      'access_key': args.access_key,
      'access_secret': args.access_secret
    },
    'services': [
      {
        'name': 'amuseable-avocado',
        'template': {
          'workload_type': 'CPU',
          'containers': [
            {
              'name': 'amuseable-avocado',
              'image': 'ghcr.io/weishi-db/lakehouse-apps:avocado-app',
              'ports': [
                {
                  'name': 'app-http',
                  'container_port': 8030,
                  'protocol': 'TCP'
                }
              ],
              'env': [
                {
                  'name': 'MY_MESSAGE',
                  'value': 'Ripe for a giggle!'
                }
              ]
            }
          ]
        }
      }
    ]
  }
}

r = requests.post(url=url, headers=headers, json=body)

print(r.status_code)
print(r.json())
print(f'App name: {app_name}')

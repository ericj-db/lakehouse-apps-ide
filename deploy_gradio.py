import requests
import argparse
import uuid

parser = argparse.ArgumentParser()
parser.add_argument('--dry_run', action='store_true')
parser.add_argument('--host', help='Databricks host to deploy app to', default='dbc-e2ec9f4b-f2a7.dev.databricks.com')
parser.add_argument('--pat', help='Personal Access Token to use for deployment', default='')
# Can possibly get this directly from github workflow
parser.add_argument('--access_key', help='Github access key to pass to Harbor', default='ericj-db')
parser.add_argument('--access_secret', help='Github access secret to pass to Harbor', default='')
parser.add_argument('--app_name', help='Name of app to deploy', default='')

args = parser.parse_args()

if args.dry_run:
    print('Dry run, exiting...')
    exit(0)

print('Not a dry run, continuing...')
if args.pat == '':
    print('No PAT provided, exiting...')
    exit(1)
else:
    print('PAT provided, continuing...')

if args.access_secret == '':
    print('No access secret provided, exiting...')
    exit(1)
else:
    print('Access secret provided, continuing...')

if args.app_name == '':
    print('App name cannot be empty')
    exit(1)

url = f'https://{args.host}/api/2.0/preview/apps/deployments'
headers = {'Authorization': f'Bearer {args.pat}'}
body = {
  'manifest': {
    'version': '1',
    'name': args.app_name,
    'description': 'Gradio App',
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
        'name': 'gradio-app',
        'template': {
          'workload_type': 'CPU',
          'containers': [
            {
              'name': 'gradio-app',
              'image': f'ghcr.io/ericj-db/gradio-app:{args.app_name}',
              'ports': [
                {
                  'name': 'app-http',
                  'container_port': 8050,
                  'protocol': 'TCP'
                }
              ],
              'env': [
                {
                  'name': "GRADIO_SERVER_PORT",
                  'value': 8050
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
print(r.content)
print(r.json())
if 300 > r.status_code >= 200:
    print(args.app_name + ' successfully deployed')

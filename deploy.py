import requests
import argparse
import uuid

parser = argparse.ArgumentParser()
parser.add_argument('--dry_run', default=True)
parser.add_argument('--host', help='Databricks host to deploy app to', default='dbc-e2ec9f4b-f2a7.dev.databricks.com')
parser.add_argument('--pat', help='Personal Access Token to use for deployment', default='')
# Can possibly get this directly from github workflow
parser.add_argument('--access_key', help='Github access key to pass to Harbor', default='ericj-db')
parser.add_argument('--access_secret', help='Github access secret to pass to Harbor', default='')

args = parser.parse_args()

if args.dry_run:
    exit(0)

app_id = uuid.uuid4().hex
url = f'https://{args.host}/api/2.0/preview/apps/deployments'
headers = {'Authorization': f'Bearer {args.pat}'}
body = {
  'resources': [
    {
      'name': 'spark-cluster',
      'option': 'EXISTING',
      'value': '1113-230645-ilkhmsih'
    }
  ],
  'manifest': {
    'version': '1',
    'name': f'ide-app-{app_id}',
    'description': 'Cluster App',
    'ingress': {
      'endpoints': [
        {
          'port_name': 'app-http',
          'visibility': 'EXTERNAL'
        }
      ]
    },
    'dependencies': [
      {
        'name': 'spark-cluster',
        'description': 'Spark cluster to transform data',
        'params': [
          {
            'key': 'runtime',
            'value': '14.1 ML'
          },
          {
            'key': 'worker type',
            'value': 'i3.xlarge'
          }
        ],
        'type': 'cluster',
        'permissions': [
          'CAN_MANAGE'
        ],
        'optional': False
      }
    ],
    'registry': {
      'url': 'https://ghcr.io',
      'access_key': args.access_key,
      'access_secret': args.access_secret
    },
    'services': [
      {
        'name': 'cluster-app',
        'template': {
          'workload_type': 'CPU',
          'containers': [
            {
              'name': 'cluster-app',
              'image': 'ghcr.io/ericj-db/lakehouse-apps-ide:main',
              'command': [
                '/databricks/nginx/init.sh'
              ],
              'ports': [
                {
                  'name': 'app-http',
                  'container_port': 8050,
                  'protocol': 'TCP'
                }
              ],
              'env': [
                {
                  'name': 'REACT_APP_CLUSTER_ID',
                  'value_from': 'spark-cluster'
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
print(f'App name: {app_id}')

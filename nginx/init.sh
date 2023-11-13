#!/usr/bin/env bash

# Extract web frontend from the build.tar file to /dist sub-folder, then move all the contents one folder up and do some cleanup
tar -xf /databricks/web/build.tar -C /databricks/web
mv /databricks/web/dist/* /databricks/web/
rm -r /databricks/web/dist/
rm /databricks/web/._dist
rm /databricks/web/build.tar
# Wire in React runtime variables
sed -i 's#__REACT_APP_CLUSTER_ID__#'"$REACT_APP_CLUSTER_ID"'#g' /databricks/web/env.js

# Initialize NGINX, make sure the log folder exists,
# disable imklog (to prevent rsyslogd from writing to /var/log/kern.log),
# substitute environment variables in the NGINX config file, start rsyslogd and cron, and finally start NGINX
mkdir -p /databricks/logs/nginx &&
sed -i '/imklog/s/^/#/' /etc/rsyslog.conf &&
envsubst '${DATABRICKS_HOST}' < "/databricks/nginx/template_nginx.conf" > "/databricks/nginx/nginx.conf" &&
rsyslogd && cron && touch /etc/crontab &&
cat "/databricks/nginx/nginx.conf" &&
exec /usr/local/bin/nginx -c "/databricks/nginx/nginx.conf" -g "daemon off;"

FROM ghcr.io/ericj-db/cluster-app:latest
COPY ./web/build.tar /databricks/web/build.tar
COPY ./nginx /databricks/nginx
CMD ["/bin/sh"]

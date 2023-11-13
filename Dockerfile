FROM ghcr.io/ericj-db/cluster-app:latest
COPY ./web/build.tar /databricks/web/build.tar
CMD ["/bin/sh"]

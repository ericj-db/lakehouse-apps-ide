FROM ghcr.io/ericj-db/cluster-app:latest
RUN apk update && apk add bash
CMD ["/bin/sh"]

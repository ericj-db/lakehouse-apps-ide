FROM node:18-alpine
RUN apk update && apk add bash
CMD ["/bin/sh"]

FROM alpine:3.19.0

LABEL maintainer="Michael Oberdorf IT-Consulting <info@oberdorf-itc.de>"
LABEL site.local.program.version="1.0.2"

# LOGLEVEL can be one of debug, info, warning , error
ENV LOGLEVEL info

COPY --chown=root:root /src /

RUN apk upgrade --available --no-cache --update \
    && apk add --no-cache --update \
       python3=3.11.6-r1 \
       py3-pip=23.3.1-r0 \
       py3-requests=2.31.0-r1

USER 2128:2128

# Start Server
ENTRYPOINT ["python3"]
CMD ["-u", "/app/monitoring.py"]

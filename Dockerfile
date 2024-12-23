FROM alpine:3.21.0

LABEL maintainer="Michael Oberdorf IT-Consulting <info@oberdorf-itc.de>"
LABEL site.local.program.version="1.1.1"

# LOGLEVEL can be one of debug, info, warning , error
ENV LOGLEVEL=info

COPY --chown=root:root /src /

RUN apk upgrade --available --no-cache --update \
    && apk add --no-cache --update \
       python3=3.12.8-r1 \
       py3-requests=2.32.3-r0

USER 2128:2128

# Start Server
ENTRYPOINT ["python3"]
CMD ["-u", "/app/monitoring.py"]

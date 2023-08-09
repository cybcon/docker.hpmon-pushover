FROM alpine:3.18.2

LABEL maintainer="Michael Oberdorf IT-Consulting <info@oberdorf-itc.de>"
LABEL site.local.program.version="1.0.0"

# LOGLEVEL can be one of debug, info, warning , error
ENV LOGLEVEL info

COPY --chown=root:root /src /

RUN apk upgrade --available --no-cache --update \
    && apk add --no-cache --update \
       python3=3.11.4-r0 \
       py3-pip=23.1.2-r0 \
    && pip3 install --no-cache-dir -r /requirements.txt

USER 2128:2128

# Start Server
ENTRYPOINT ["python3"]
CMD ["-u", "/app/monitoring.py"]

FROM python:3.6.4-alpine3.7

ENV WEB_CONCURRENCY=4
ENV GEOLITE="/airq/GeoLite2-City_20180306/GeoLite2-City.mmdb"

ADD . /airq

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories && \
apk add -U ca-certificates libffi libstdc++ && \
apk add --virtual build-deps build-base libffi-dev && \
    # Pip
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn /airq && \
    # Cleaning up
    apk del build-deps && \
    rm -rf /var/cache/apk/*

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "airq:app"]

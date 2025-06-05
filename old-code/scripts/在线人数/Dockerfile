FROM python:3.9-alpine

WORKDIR /home/app
COPY . /home/app

RUN apk add --no-cache gcc musl-dev libffi-dev python3-dev cython curl \
    && pip install --upgrade pip setuptools wheel

RUN  apk add --no-cache shadow && \
     pip install --upgrade pip && \
     pip3 install -r requirements.txt && \
     groupadd appgroup && useradd app -G appgroup && \
     chown -R app:appgroup /home/app 

EXPOSE 8080

CMD ["/usr/local/bin/gunicorn","-c","gunicorn_config.py","app:app"]


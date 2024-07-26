FROM public.ecr.aws/docker/library/python:3.11.9

RUN apt update && apt install -y supervisor gcc musl-dev python3-dev dos2unix curl nginx && \
    rm -rf /var/lib/apt/lists/*

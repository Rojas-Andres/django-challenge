FROM public.ecr.aws/docker/library/python:3.11.9

RUN apt update && apt install -y supervisor dos2unix curl && \
    rm -rf /var/lib/apt/lists/*

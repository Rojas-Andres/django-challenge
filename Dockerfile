FROM public.ecr.aws/f5k9u7m7/ecr_template_python_fargate

ARG ENVIRONMENT=default
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY ./src /usr/src/app/

COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY ./requirements /usr/src/app/requirements/

RUN pip install --upgrade pip && \
    pip install -r requirements/prod.txt

RUN dos2unix /usr/local/bin/start.sh

EXPOSE 8000
ENTRYPOINT ["start.sh"]

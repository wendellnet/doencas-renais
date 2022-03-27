FROM python:3.9

LABEL MAINTAINER="Wendell Lopes do Nascimento <wendell@onservicetech.com.br>"

ENV GROUP_ID=1000 \
    USER_ID=1000


RUN apt-get update; \
    apt-get -y upgrade; \
    apt-get install -y gnupg2 wget lsb-release 

COPY . /var/www
WORKDIR /var/www
ENV PATH=$PATH:/var/www
ENV PYTHONPATH /var/www
RUN wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN    groupadd --gid $GROUP_ID app                                        \
    && useradd --create-home --uid $USER_ID --shell /bin/sh --gid app app

USER $USER_ID:$GROUP_ID

USER app

EXPOSE 5000

#ENTRYPOINT ["python3", "-u", "app.py"]

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]

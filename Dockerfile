FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG var_name 
ENV env_var_name=$var_name

WORKDIR /usr/src/app

COPY . .

RUN apt-get -y clean\
    && apt-get -y update\
    && apt-get install -y ffmpeg flac

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

#CMD ["python", "./generator/manage.py", "runserver"]

CMD gunicorn --timeout 10000 -b 0.0.0.0:$PORT generator.wsgi:application
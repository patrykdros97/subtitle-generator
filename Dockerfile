FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY . .

RUN apt-get -y update\
    && apt-get install -y ffmpeg flac

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

#CMD ["python", "./generator/manage.py", "runserver"]

CMD gunicorn -b 0.0.0.0:$PORT generator.wsgi:application
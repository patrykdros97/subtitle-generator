FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN apt-get -y update\
    && apt-get install -y ffmpeg flac

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

CMD ["python", "./generator/manage.py", "runserver", "0.0.0.0:$PORT"]
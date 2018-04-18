FROM python:3.6-alpine 

RUN adduser -D labfriday

WORKDIR /home/labfriday

COPY requirements.txt requirements.txt
RUN python -m venv venv

RUN apk add --update curl gcc g++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY labfriday.db ./  
COPY app app
COPY migrations migrations
COPY labfriday.py config.py boot.sh ./

RUN chmod +x boot.sh

ENV FLASK_APP labfriday.py

RUN chown -R labfriday:labfriday ./
USER labfriday

EXPOSE 8080
ENTRYPOINT ["./boot.sh"]

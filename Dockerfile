FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY cron_scheduler.sh ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["cron_scheduler.sh" ]

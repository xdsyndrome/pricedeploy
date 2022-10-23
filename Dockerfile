FROM python:3.7

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ADD ./models ./models
ADD server.py server.py

# Expose Port 5000 in docker container
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]
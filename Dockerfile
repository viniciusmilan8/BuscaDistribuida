FROM python:3.12-alpine

COPY ./ /app/
WORKDIR /app/

RUN pip install -r /app/requirements.txt

CMD exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload

FROM python:3.8-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]

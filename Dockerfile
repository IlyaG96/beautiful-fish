FROM python:3.9.10-alpine

RUN mkdir "/usr/src/fishapp"

WORKDIR /usr/src/fishapp
COPY requirements.txt /usr/src/fishapp/

RUN pip install --no-cache-dir -r requirements.txt
COPY . .


ENTRYPOINT ["python"]
CMD ["bot.py"]

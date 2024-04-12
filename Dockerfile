FROM python:latest


ENV PYTHONUNBUFFERED 1

RUN mkdir /newsapi
WORKDIR /newsapi
COPY . /newsapi
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver"]
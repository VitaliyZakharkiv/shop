FROM python:3.8.1

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

#WORKDIR /Programming/програмінг/Проекти/BLOG/shop
WORKDIR /usr/src/shop

#COPY requirements.txt /Programming/програмінг/Проекти/BLOG/shop/requirements.txt
COPY requirements.txt ./

#RUN pip install -r /Programming/програмінг/Проекти/BLOG/shop/requirements.txt
RUN pip install -r requirements.txt

#COPY . /Programming/програмінг/Проекти/BLOG/shop
COPY . /usr/src/shop

EXPOSE 8000
CMD['python', 'manage.py', 'runserver', '0.0.0.0:8000']


# base python image
FROM python:3.5.7-alpine3.8

# set working directory
WORKDIR '/app'

# run all installs in the 
RUN pip3 install flask requests flask_cors gunicorn

# move backend directory into root of app directory
# OK b/c backend image contains no frontend code
COPY ./ ./
# expost 5005 and spawn gunicorn on 5005 with flask app
EXPOSE 5005
# please do not include the secret key in the dockerfile
# use another form of secrets for the environmental variable
ENV DJANGO_SECRET_KEY='my_prod_django_secret'
CMD ["gunicorn", "--bind", "0.0.0.0:5005", "--workers", "4", "api.v1.app:app"]

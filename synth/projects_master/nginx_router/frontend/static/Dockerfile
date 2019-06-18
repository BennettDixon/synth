# PRODUCTION DOCKER FILE

# for use in creating production builds
# this NGINX container is used to serve static content

FROM nginx

# copy the nginx server configuration
COPY ./nginx_conf/default.conf /etc/nginx/conf.d/default.conf
COPY ./nginx_conf/nginx.conf /etc/nginx/nginx.conf

# copy static content
COPY ./*.html /usr/share/nginx/html
COPY ./styles /usr/share/nginx/html/styles
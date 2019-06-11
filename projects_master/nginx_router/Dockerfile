# PRODUCTION DOCKER FILE

# currently same as development dockerfile for this container

# for use in creating production builds
# nginx is used as router for all containers
# and is the only container exposed to the host

# see docker compose for forwarding information
# NGINX is configured to receive TCP traffic on port 80
# the default port forwarded to host by compose for this container:
#   - is 8800
FROM nginx

# copy the nginx server configuration
COPY ./nginx_conf/default.conf /etc/nginx/conf.d/default.conf
COPY ./nginx_conf/nginx.conf /etc/nginx/nginx.conf

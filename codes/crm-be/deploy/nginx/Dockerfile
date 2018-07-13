FROM tutum/nginx

RUN rm /etc/nginx/sites-enabled/default \
    && mkdir -p /nginx/cdn \
    && chmod 777 /nginx/cdn \
    && mkdir -p /nginx/logs \
    && echo "" >> /nginx/logs/nginx.access.log \
    && chmod 777 /nginx/logs

ADD sites-enabled/ /etc/nginx/sites-enabled

FROM nginx:latest


RUN mkdir -p /etc/letsencrypt/live/k4b205.p.ssafy.io

COPY ./ssl/fullchain.pem /etc/letsencrypt/live/k4b205.p.ssafy.io/fullchain.pem
COPY ./ssl/privkey.pem /etc/letsencrypt/live/k4b205.p.ssafy.io/privkey.pem
COPY ./ssl/options-ssl-nginx.conf /etc/letsencrypt/options-ssl-nginx.conf
COPY ./ssl/ssl-dhparams.pem /etc/letsencrypt/ssl-dhparams.pem

COPY ./default.conf  /etc/nginx/conf.d/default.conf

COPY ./front.conf  /etc/nginx/conf.d/front.conf

RUN mkdir -p /var/www/media
RUN mkdir -p /var/www/static

WORKDIR /var/www/media
RUN chown -R nginx:nginx /var/www/media


WORKDIR /var/www/static
RUN chown -R nginx:nginx /var/www/static
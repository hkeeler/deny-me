FROM matter/shibboleth-nginx

RUN apt-get update && \
    apt-get -y install vim git && \
    mkdir /etc/nginx/ssl && \
    openssl req -x509 -nodes -newkey rsa:2048 -keyout /etc/nginx/ssl/temp.key -out /etc/nginx/ssl/temp.crt -subj "/C=US/ST=California/L=Sacramento/CN=www.fakesite.org/emailAddress=admin@fakesite.org" && \
    ln -s /etc/nginx/ssl/temp.key /etc/nginx/ssl/cert.key && \
    ln -s /etc/nginx/ssl/temp.crt /etc/nginx/ssl/cert.crt && \
    git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt && \
    shib-keygen -f

#    cd /opt/letsencrypt && \
#    ./letsencrypt-auto certonly --manual --non-interactive --agree-tos --email hkeeler+letsencrypt@gmail.com -d deny-me-nginx.hkeeler.svc.tutum.io
    
COPY conf /


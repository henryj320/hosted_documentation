FROM nginx

# COPY Vault /usr/share/nginx/html
# RUN mkdir -p Vault
ADD ./Vault /Vault

COPY ./Config /usr/share/nginx/html/Config

RUN mkdir -p /Pages

# CMD ["python3", "main.py"]

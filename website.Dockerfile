FROM nginx

# COPY Vault /usr/share/nginx/html
# RUN mkdir -p Vault
ADD ./Vault /Vault

RUN mkdir -p /Pages

# CMD ["python3", "main.py"]

FROM nginx

COPY Vault /usr/share/nginx/html

RUN mkdir -p /Pages

# CMD ["python3", "main.py"]
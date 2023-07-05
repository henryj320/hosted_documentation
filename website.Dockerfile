FROM nginx

ADD ./Vault /Vault

# Copy the CSS.
COPY ./Config /usr/share/nginx/html/Config

# Copy all images into their respective folders
COPY ./**/*.png /usr/share/nginx/html
COPY ./**/*.jpg /usr/share/nginx/html
COPY ./**/*.jpeg /usr/share/nginx/html
COPY ./**/*.gif /usr/share/nginx/html

RUN mkdir -p /Pages

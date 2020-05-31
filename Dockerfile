# Dockerfile for creating a deployment

# build
FROM node:13.10.1-alpine as build-react
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
ENV NODE_ENV production
ENV REACT_APP_TRIVIA_SERVICE_URL $REACT_APP_TRIVIA_SERVICE_URL
COPY ./services/client/package*.json ./
RUN npm install
RUN npm install react-scripts@3.4.0
COPY ./services/client .
RUN npm run build

# production
FROM nginx:stable-alpine as production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV=production
ENV APP_SETTINGS=project.config.ProductionConfig
WORKDIR /app
RUN apk update && \
    apk add --no-cache --virtual build-deps \
    openssl-dev libffi-dev gcc python3-dev musl-dev \
    postgresql-dev netcat-openbsd
RUN python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache
COPY --from=build-react /app/build /usr/share/nginx/html
COPY ./services/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./services/trivia/requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY ./services/trivia .
CMD gunicorn -b 0.0.0.0:5000 manage:app --daemon && \
    sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
    nginx -g 'daemon off;'
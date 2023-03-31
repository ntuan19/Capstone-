FROM python:3-alpine
RUN apk add --no-cache libffi-dev
RUN apk add --no-cache gcc musl-dev linux-headers \
    && pip install --upgrade pip

WORKDIR /working
COPY requirements.txt /working/
RUN pip install -r requirements.txt

COPY . /working/
WORKDIR /working/backend
RUN export FLASK_APP=app.py \
    && export FLASK_DEBUG=1 \
    && python -m flask run 
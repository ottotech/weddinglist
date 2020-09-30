FROM python:3.7.4

ENV PYTHONUNBUFFERED=1

# Setup the Django app.
RUN mkdir /weddinglist
COPY . /weddinglist
WORKDIR /weddinglist
RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

# Start processes.
RUN ["chmod", "+x", "/weddinglist/dev-docker-entrypoint.sh"]
CMD ["/weddinglist/dev-docker-entrypoint.sh"]
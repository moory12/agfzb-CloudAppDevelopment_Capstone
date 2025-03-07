FROM python:3.8.2

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y netcat

ENV APP=/App

# Change the workdir.
WORKDIR $APP

# Install the requirements
COPY server/requirements.txt $APP
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the files
COPY . $APP

EXPOSE 8000

RUN chmod +x /App/entrypoint.sh
ENTRYPOINT ["/App/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]
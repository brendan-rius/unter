FROM python:3.5

RUN mkdir /app
WORKDIR /app

# We launch pip install only if the requirements have changed
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "unter"]
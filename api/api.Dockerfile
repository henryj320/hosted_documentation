FROM python:3.8-slim-buster

ADD ./Vault /Vault

COPY api/requirements.txt requirements.txt

RUN pip3 install --upgrade build

RUN pip3 install -r requirements.txt

COPY api/main.py main.py


# CMD ["python3", "basic_viewer/api.py"]

CMD ["python3", "main.py"]

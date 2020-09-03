FROM python:3

WORKDIR /flask_first_project

COPY . /flask_first_project

RUN pip install -r setup.txt

ENTRYPOINT ["python"]

CMD ["run.py"]

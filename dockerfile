FROM python:3

WORKDIR /first_project

COPY . /first_project

RUN pip install -r setup.txt

ENTRYPOINT ["python"]

CMD ["run.py"]

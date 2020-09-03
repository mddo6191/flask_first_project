FROM python:3

#create app directory
WORKDIR /app

#install app dependencies
COPY src/requirements.txt ./

RUN pip install -r requirements.txt

#bundle app source
COPY src /app

ENTRYPOINT ["python"]

CMD ["run.py"]

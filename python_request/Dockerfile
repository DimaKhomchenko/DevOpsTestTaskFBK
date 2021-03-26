FROM python:3-slim
RUN pip3 install psycopg2-binary
COPY main.py /
EXPOSE 8080
CMD [ "python3", "./main.py" ]
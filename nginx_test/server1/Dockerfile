FROM python:3
COPY ../../requirements.txt /requirements.txt
WORKDIR /
RUN pip install -r requirements.txt
COPY ../.. /
ENTRYPOINT ["python"]
CMD ["server1.py"]
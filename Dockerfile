FROM python:3.9.5

WORKDIR /


COPY requirements.txt /
RUN pip install -r requirements.txt


COPY templates /templates
COPY app.py main.py /


EXPOSE 5000
CMD ["python", "main.py"]
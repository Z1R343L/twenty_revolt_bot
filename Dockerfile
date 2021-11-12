FROM python:bullseye
COPY . .
RUN pip install -U setuptools wheel -vv
RUN pip install -r requirements.txt
CMD ["python3", "-u", "main.py"]

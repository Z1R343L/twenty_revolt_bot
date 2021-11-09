FROM python:bullseye
COPY . .
RUN pip install -q -r requirements.txt > /dev/null 2>&1
CMD ["python3", "-u", "main.py"]

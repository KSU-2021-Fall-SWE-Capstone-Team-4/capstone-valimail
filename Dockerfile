FROM python:3.9

LABEL imageAuthor = "brooklyn@apps.com"

WORKDIR /opt/capstone-valimail

COPY . .

# wont be saved to temp file
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]


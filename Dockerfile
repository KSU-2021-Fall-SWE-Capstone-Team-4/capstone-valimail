FROM python:3.9
# python:3.8.10
# version change

LABEL imageAuthor = "brooklyn@apps.com"

COPY . /opt/AuthMiddleware

RUN apt-get update
RUN apt-get install python3 python3-pip python3-dev -y

WORKDIR /opt/AuthMiddleware
RUN pip install -r requirements.txt

EXPOSE 5000

RUN chmod +x /opt/AuthMiddleware/main.py
#RUN pip install

#ENTRYPOINT ["/opt/mpp-solar/setup.py","root","AuthMiddleware"]
RUN ls /opt
CMD ["/opt/AuthMiddleware/main.py","root","AuthMiddleware"]


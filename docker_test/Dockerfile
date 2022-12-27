FROM python:3.9

ADD requirements.txt /
# install popular Python packages
RUN pip3 install -r requirements.txt

ADD main.py /

EXPOSE 80

CMD [ "python3", "./main.py" ]
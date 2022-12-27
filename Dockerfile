FROM python:3.9

ADD requirements.txt /
# install popular Python packages
RUN pip3 install -r requirements.txt

ADD app /app
ADD main.py /

CMD [ "python3", "./main.py" ]
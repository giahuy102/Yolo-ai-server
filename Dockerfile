FROM python:3.8

WORKDIR /usr/app

RUN pip install --no-cache-dir --timeout 1000 torch>=1.7.0,!=1.12.0 torchvision>=0.8.1,!=0.13.0

COPY requirements.txt .

RUN pip install --no-cache-dir --timeout 1000 -r requirements.txt

COPY . .

EXPOSE 5005

CMD [ "python3", "-u", "app.py" ]

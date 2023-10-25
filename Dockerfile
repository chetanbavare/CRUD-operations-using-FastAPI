#code imported from docker hub>python image

FROM python:3.9.10 
#image version

WORKDIR /usr/src/app
#to provide directory

COPY requirements.txt ./
#important step as installing dependencies is longest process , so need to make it cache

RUN pip install --no-cache-dir -r requirements.txt
#now run the command to install

COPY . .
#copy into the image file

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
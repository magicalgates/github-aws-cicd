FROM python:3.8-slim
RUN mkdir -p /function
WORKDIR /function

RUN apt-get update
RUN apt-get install -y \
    libgtk2.0-dev \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev

RUN apt-get install -y awscli
RUN apt-get install -y uuid-runtime
RUN apt-get install -y default-mysql-client
RUN apt-get install -y libmariadb-dev
RUN apt-get install -y libssl-dev

RUN pip install --target /function awslambdaric

COPY /dbscript.sh /function
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
RUN chmod 755 /usr/bin/aws-lambda-rie
COPY entry.sh /
COPY app.py /function/
COPY dbscript.sh /function/
COPY rds-combined-ca-bundle.pem /function/
RUN chmod +x /function/dbscript.sh
RUN chmod +x /entry.sh
ENTRYPOINT [ "/entry.sh" ]
#ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
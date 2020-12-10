FROM public.ecr.aws/lambda/python:3.8
#RUN yum install python3-distutils
#Required for grpcio on this specific image
#RUN pip install --upgrade distutils
#RUN yum install gcc gcc-c++ kernel-devel make -y
#RUN yum downgrade python36-libs-3.6.8-1.el7.x86_64
#RUN yum install -y python36-devel.x86_64

COPY deployment/app.py deployment/creds.json requirements.txt ./
RUN pip3 install -r requirements.txt
CMD ["app.lambdaHandler"]
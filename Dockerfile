FROM public.ecr.aws/amazonlinux/amazonlinux:latest AS myPortfolio

WORKDIR /home/myCv/

COPY ./ /home

RUN yum install -y python3-pip
RUN python3 -m pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
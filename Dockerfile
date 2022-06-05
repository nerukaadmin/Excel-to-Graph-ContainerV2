FROM python:3.7-slim-buster
WORKDIR /excel
COPY ex_to_graph.py /excel/
COPY requirements.txt /excel
RUN mkdir -p /excel/IN
RUN mkdir -p /excel/OUT
RUN mkdir -p /excel/tmp
RUN mkdir -p /excel/TM
RUN mkdir -p /excel/ROLE
RUN mkdir -p /excel/ROLE_TXT
RUN ls /excel
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python" ,"ex_to_graph.py"]
CMD ["a"]

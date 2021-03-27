FROM public.ecr.aws/lambda/python:3.8

RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install pandas
RUN python3.8 -m pip install aws-wsgi
RUN python3.8 -m pip install dash
RUN python3.8 -m pip install plotly-express
RUN python3.8 -m pip install dash-core-components
RUN python3.8 -m pip install dash_html_components

COPY server.py   ./
CMD ["server.handler"]

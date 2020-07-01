FROM continuumio/miniconda3:latest

ADD environment.yml /environment.yml

RUN conda update conda
RUN conda env create
SHELL ["conda", "run", "-n", "hyo", "/bin/bash", "-c"]

RUN mkdir /backend

ADD ./backend /backend
ADD wsgi.py /wsgi.py
ADD keep_awake.py /keep_awake.py

ENTRYPOINT ["conda", "run", "-n", "hyo", "python", "wsgi.py"]

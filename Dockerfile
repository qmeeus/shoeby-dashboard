FROM python:3.6.5

RUN pip install --upgrade pip

ARG USER_ID
RUN useradd --uid $USER_ID --shell /bin/bash --create-home patrick

USER patrick

RUN mkdir -p /home/patrick/project/data
WORKDIR /home/patrick/project

COPY --chown=patrick:users . /home/patrick/project/

VOLUME ["/home/patrick/project/data"]

ENV PATH="/home/patrick/.local/bin:$PATH"
RUN pip install -r requirements.txt --user

EXPOSE 8050

ENTRYPOINT ["python", "dashboard.py"]
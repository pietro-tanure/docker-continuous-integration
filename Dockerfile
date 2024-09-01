# Dockerfile

FROM python:3.11.2-slim-bullseye

RUN apt-get update && \
    apt-get upgrade --yes

RUN useradd --create-home realpython
USER realpython
WORKDIR /home/realpython

ENV VIRTUALENV=/home/realpython/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --chown=realpython requirements.txt ./
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY --chown=realpython src/ src/
COPY --chown=realpython test/ test/

RUN python -m pip install -r requirements.txt

CMD ["flask", "--app", "page_tracker.app", "run", \
    "--host", "0.0.0.0", "--port", "5000"]

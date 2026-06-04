FROM python:3.13-slim AS builder
WORKDIR /usr/app
COPY src/requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN  pip install --upgrade pip && \ 
    pip install --no-cache-dir -r requirements.txt 

FROM python:3.13-slim AS final
WORKDIR /usr/app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN useradd -m monitor && chown monitor:monitor /usr/app
USER monitor
COPY --chown=monitor:monitor ./src /usr/app
EXPOSE 8000
CMD [ "python","-u", "main.py"]
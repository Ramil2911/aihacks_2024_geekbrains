#
FROM python:3.9

COPY ./api /app

EXPOSE 8001

RUN --mount=type=cache,target=/root/.cache \
    pip install -r /app/requirements.txt

CMD ["uvicorn", "app.api_run:app", "--host", "0.0.0.0", "--port", "8001"]
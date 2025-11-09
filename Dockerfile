FROM python:3.14
WORKDIR /code
COPY ./pyproject.toml /code/pyproject.toml
RUN pip install --no-cache-dir --upgrade /code
COPY ./build/lib/app /code/app
COPY ./build/lib/mlcore /code/mlcore
CMD ["fastapi", "run", "app/main.py", "--port", "80"]

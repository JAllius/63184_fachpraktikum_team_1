FROM python:3.14
WORKDIR /code
COPY ./pyproject.toml /code/pyproject.toml
RUN pip install --no-cache-dir --upgrade -r /code/pyproject.toml
COPY ./build/lib/app /code/app
CMD ["fastapi", "run", "app/main.py", "--port", "80"]

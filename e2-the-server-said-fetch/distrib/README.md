# The Server Said Fetch — participant files

A campus URL-preview service can fetch a page on your behalf. Its staff-only
vault supposedly cannot be reached from outside. Retrieve the flag.

The bundled `server.py` is the same implementation used remotely. The provided
`flag.txt` is a placeholder, not the scoring flag.

## Run with Python

```sh
python3 server.py
```

Open <http://127.0.0.1:5000> in a browser. No pip packages are required.

## Run with Docker

```sh
docker compose up --build
```

Open <http://127.0.0.1:35006>. Only the preview server is published; the
staff-only server is bound to localhost inside the container.

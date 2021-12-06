# Python CLI template

```sh
    MVladislav
```

---

- [Python CLI template](#python-cli-template)
  - [create `.env` file](#create-env-file)
    - [development mode:](#development-mode)
    - [production mode:](#production-mode)
  - [install/startup](#installstartup)
    - [run test](#run-test)
    - [shell](#shell)
      - [debug](#debug)
    - [docker](#docker)

---

an template to copy to implement python with `setup.py` and `fastapi` for **api**.

---

## create `.env` file

depends on env mode copy the correct **.env** and change defaults you need:

### development mode:

```sh
$cp .env_template_kons .env
```

### production mode:

```sh
$cp .env_template_prod .env
```

---

## install/startup

### run test

```sh
$./tests-start.sh
```

### shell

```sh
$python3 -m pip install .
$gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:main
```

#### debug

```sh
$mkdir -p "$HOME/.vm_api"
$python3 -m venv "$HOME/.vm_api/venv"
$source "$HOME/.vm_api/venv/bin/activate"
$python3 -m pip install -e . -v
$uvicorn app.main:main --reload
```

### docker

run **docker-compose** `build` and `up`

```sh
$DOCKER_BUILDKIT=1 docker-compose build
$DOCKER_BUILDKIT=1 docker-compose up -d
```

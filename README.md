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
    - [docker](#docker)
    - [shell](#shell)
    - [DEBUG](#debug)
  - [sources](#sources)
    - [code](#code)
    - [python](#python)
    - [github](#github)
    - [examples](#examples)

---

an template to copy to implement python with `setup.py` and `fastapi` for **api**.

---

## create `.env` file

### development mode:

```env
LICENSE=GNU AGPLv3
AUTHOR=MVladislav
AUTHOR_EMAIL=info@mvladislav.online

PROJECT_NAME=vm_api_template
# PROD | KONS
ENV_MODE=KONS
VERSION=0.0.1
# NOTICE | SPAM | DEBUG | VERBOSE | INFO | NOTICE | WARNING | SUCCESS | ERROR | CRITICAL
LOGGING_LEVEL=DEBUG
# 0 - 4
LOGGING_VERBOSE=3

PROTOCOL=http
HOST=127.0.0.1
PORT=8000
ALLOW_CREDENTIALS=true
ALLOWED_METHODES=OPTIONS,GET
ALLOWED_HEADERS=*

API_PREFIX=/api/v1

TOKEN_API_NAME=x-access-token
# openssl rand -hex 64
SECRET_KEY="c1aa1118518050c4173c8c991e407c5a97f61010e2d27399568b7fcacec9892f7b34fcf3e32ba30ae6fb64c1219625d915b7cdda253a5888f1ce305194030f75"
ALGORITHM=HS512
ACCESS_TOKEN_EXPIRE_MINUTES=30

ACCOUNT_REGISTER_EXPIRE_MINUTES=5

TOTP_DIGITS=6
TOTP_INTERVAL=30
TOTP_VALIDE_WINDOW=0

QR_VERSION=1
QR_BOX_SIZE=10
QR_BORDER=5
# QR_FACTORY=none
QR_FILLED=false
QR_FIT=true

# mongodb | mongodb+srv
DB_PROTOCOL=mongodb
# DB_HOST=mongo
DB_HOST=localhost
DB_PORT=27017
DB_SCHEMA=test01
# DB_URL=none
# DB_USER=admin
# DB_PASSWORD=swordfish
```

### production mode:

```env
LICENSE=GNU AGPLv3
AUTHOR=MVladislav
AUTHOR_EMAIL=info@mvladislav.online

PROJECT_NAME=vm_api_template
# PROD | KONS
ENV_MODE=PROD
VERSION=0.0.1
# NOTICE | SPAM | DEBUG | VERBOSE | INFO | NOTICE | WARNING | SUCCESS | ERROR | CRITICAL
LOGGING_LEVEL=INFO
# 0 - 4
LOGGING_VERBOSE=2

PROTOCOL=http
HOST=127.0.0.1
PORT=8000
ALLOW_CREDENTIALS=true
ALLOWED_METHODES=OPTIONS,GET
ALLOWED_HEADERS=*

API_PREFIX=/api/v1

TOKEN_API_NAME=x-access-token
# openssl rand -hex 64
SECRET_KEY="<ADD SECRET HERE>"
ALGORITHM=HS512
ACCESS_TOKEN_EXPIRE_MINUTES=43800

ACCOUNT_REGISTER_EXPIRE_MINUTES=5

TOTP_DIGITS=6
TOTP_INTERVAL=30
TOTP_VALIDE_WINDOW=0

QR_VERSION=1
QR_BOX_SIZE=10
QR_BORDER=5
# QR_FACTORY=none
QR_FILLED=false
QR_FIT=true

# mongodb | mongodb+srv
DB_PROTOCOL=mongodb
DB_HOST=mongo
DB_PORT=27017
DB_SCHEMA=test01
# DB_URL=none
DB_USER=admin
DB_PASSWORD=swordfish
```

---

## install/startup

### docker

run **docker-compose** `build` and `up`

```sh
$DOCKER_BUILDKIT=1 docker-compose build
$DOCKER_BUILDKIT=1 docker-compose up -d
```

### shell

> `starlette` must be installed before project can be installed
>
> `setup.py` looks into `app/utils/config.py` which use `config` from `starlette`

```sh
$pip3 install starlette && pip3 install .
$gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:main
```

### DEBUG

```sh
$python3 -m venv ./venv
$source venv/bin/activate
$pip3 install starlette && pip3 install --editable .
$uvicorn app.main:main --reload
```

---

## sources

### code

- <https://fastapi.tiangolo.com>
- <https://github.com/encode/uvicorn>
- <https://github.com/on1arf/gr-pocsag>

### python

- <https://stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools>

### github

- <https://zellwk.com/blog/github-actions-deploy/>
- <https://github.com/actions/create-release>
- <https://github.com/marketplace/actions/create-env-file>
- <https://docs.github.com/en/actions/guides/storing-workflow-data-as-artifacts>
- <https://www.section.io/engineering-education/setting-up-cicd-for-python-packages-using-github-actions/>
- <https://docs.github.com/en/actions/reference/context-and-expression-syntax-for-github-actions#example-printing-context-information-to-the-log-file>
- <https://github.community/t/possible-to-use-conditional-in-the-env-section-of-a-job/135170>

### examples

- [mongodb](https://gist.github.com/fatiherikli/4350345)
- [mongodb](https://github.com/mongodb-developer/mongodb-with-fastapi)
- [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- [fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app)
- [uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)

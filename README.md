# Python CLI template

```sh
    MVladislav
```

---

- [Python CLI template](#python-cli-template)
  - [TODO:](#todo)
  - [on clone this project](#on-clone-this-project)
  - [code quality and git](#code-quality-and-git)
    - [pre-commit](#pre-commit)
  - [sources](#sources)
    - [code](#code)
    - [python](#python)
    - [github](#github)
    - [examples](#examples)

---

## TODO:

- [ ] add ci-cd workflow
- [ ] add email template usage
- [ ] add default frontend
- [ ] ...

---

WORK IN PROGRESS

an template to copy to implement python with `setup.py` and `fastapi` for **api**.

---

## on clone this project

change to your project name:

```sh
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/scripts/setup-dev.sh 2>/dev/null
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/scripts/setup.sh 2>/dev/null
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/app/utils/config.py 2>/dev/null
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/.env 2>/dev/null
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/.env_project 2>/dev/null
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/.env_template_kons 2>/dev/null
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/.env_template_prod 2>/dev/null
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/docker-compose.yaml 2>/dev/null
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/Dockerfile 2>/dev/null
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/pyproject.toml 2>/dev/null
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/README.md 2>/dev/null
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/setup.cfg 2>/dev/null
$sed -i "s|vm_api|<PROJECT_NAME>|g" ./backend/setup.py 2>/dev/null

$mv app <PROJECT_NAME>
$sed -i "s|app\b|<PROJECT_NAME>|g" ./backend/.gitignore 2>/dev/null
$sed -i "s|app\b|<PROJECT_NAME>|g" ./backend/.dockerignore 2>/dev/null
$sed -i "s|app\b|<PROJECT_NAME>|g" .pre-commit-config.yaml 2>/dev/null
$sed -i "s|app\b|<PROJECT_NAME>|g" ./backend/docker-compose.yaml 2>/dev/null
$sed -i "s|app\b|<PROJECT_NAME>|g" ./backend/pyproject.toml 2>/dev/null
$sed -i "s|app\b|<PROJECT_NAME>|g" ./backend/setup.cfg 2>/dev/null
$sed -i "s|app\b|<PROJECT_NAME>|g" ./backend/setup.py 2>/dev/null
$sed -i "s|app\b|<PROJECT_NAME>|g" ./backend/tox.ini 2>/dev/null
$sed -i "s|app\b|<PROJECT_NAME>|g" ./backend/<PROJECT_NAME>/main.py 2>/dev/null
```

update version:

```sh
$sed -i 's|"0.0.1"|"<NEW_VERSION>"|g' ./backend/app/utils/config.py 2>/dev/null
$sed -i "s|0.0.1|<NEW_VERSION>|g" ./backend/.env_project 2>/dev/null
$sed -i "s|0.0.1|<NEW_VERSION>|g" ./backend/docker-compose.yaml 2>/dev/null
$sed -i "s|0.0.1|<NEW_VERSION>|g" ./backend/Dockerfile 2>/dev/null
$sed -i "s|0.0.1|<NEW_VERSION>|g" ./backend/pyproject.toml 2>/dev/null
$sed -i "s|0.0.1|<NEW_VERSION>|g" ./backend/setup.cfg 2>/dev/null
$sed -i "s|0.0.1|<NEW_VERSION>|g" ./backend/setup.py 2>/dev/null
```

---

## code quality and git

### pre-commit

run:

```sh
$git config --local core.hooksPath .git/hooks
$pre-commit install
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

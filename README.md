# Flask users

Initial config

Copy env_example to .env and change your config parameter.

```bash
# env_example

DEBUG=True
URL_FRONT=

TOKEN_KEY=
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

KEY_URL_TOKEN=
USERS_ACTIVATE_TOKEN_AGE_IN_SECONDS=259200
USERS_RESET_PASSWORD_TOKEN_AGE_IN_SECONDS=86400

MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_ROOT_PASSWORD=
MYSQL_PORT=3306
MYSQL_HOST=localhost

MAIL_SERVER=localhost
MAIL_PORT=25
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_USE_TLS=False
MAIL_USE_SSL=False
DONT_REPLY_FROM_EMAIL="no reply,noreply@correo.com"
ADMINS="firt.admin@example.com,second.admin@example.com"


```


Create a requirement.txt
```
pipenv install --skip-lock
pipenv run pip freeze > requirements.txt

```

Run over docker compose:
```code 
docker-composer up
```

Project documentation [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)


List of routes 
```
pipenv run routes

Endpoint                         Methods  Rule
-------------------------------  -------  ----------------------------------
app.auth.active_user_view        GET      /api/auth/active-user/<token>/
app.auth.change_password_view    POST     /api/auth/change-password/<token>/
app.auth.login_view              POST     /api/auth/login/
app.auth.password_recovery_view  POST     /api/auth/password-recovery/
app.auth.registration_user_view  POST     /api/auth/register-user/
app.users.create_user_view       POST     /api/users/
app.users.get_user_view          GET      /api/users/<int:id>/
app.users.list_users_view        GET      /api/users/
app.users.me_update_user_view    PUT      /api/users/me/update/
app.users.me_view                GET      /api/users/me/
flasgger.<lambda>                GET      /apidocs/index.html
flasgger.apidocs                 GET      /apidocs/
flasgger.apispec_1               GET      /apispec_1.json
flasgger.static                  GET      /flasgger_static/<path:filename>
static                           GET      /static/<path:filename>

```


Run unitary test
```
pipenv install
pipenv run base
pipenv run cov
pipenv run report
```

Other whise to see a report `pipenv run html` and open *htmlcov/index.html* from your browser


Coverage test result
```
❯ pipenv run cov
Loading .env environment variables...
=================================== test session starts ====================================
platform linux -- Python 3.9.2, pytest-7.2.0, pluggy-1.0.0
rootdir: /<path-folder>/flask-users/fusers-crud, configfile: pytest.ini
plugins: env-0.8.1
collected 46 items                                                                         

fusers-crud/tests/test_auth.py ......................                                [ 47%]
fusers-crud/tests/test_tools.py .                                                    [ 50%]
fusers-crud/tests/test_users.py .......................                              [100%]

=================================== 46 passed in 12.15s ====================================
❯ pipenv run report
Loading .env environment variables...
Name                                  Stmts   Miss  Cover
---------------------------------------------------------
fusers-crud/config/__init__.py            2      0   100%
fusers-crud/config/app.py                29      0   100%
fusers-crud/config/config.py             51      0   100%
fusers-crud/config/extensions.py         19      0   100%
fusers-crud/handlers/__init__.py          0      0   100%
fusers-crud/handlers/errors.py            7      0   100%
fusers-crud/middleware/__init__.py        0      0   100%
fusers-crud/middleware/jwt_token.py      15      0   100%
fusers-crud/middleware/token.py          19      0   100%
fusers-crud/models/__init__.py            0      0   100%
fusers-crud/models/users.py              12      0   100%
fusers-crud/routers/__init__.py           0      0   100%
fusers-crud/routers/auth.py               8      0   100%
fusers-crud/routers/routers.py            6      0   100%
fusers-crud/routers/users.py              8      0   100%
fusers-crud/schemas/__init__.py           0      0   100%
fusers-crud/schemas/auth.py              43      0   100%
fusers-crud/schemas/users.py             17      0   100%
fusers-crud/tests/__init__.py             0      0   100%
fusers-crud/tests/conftest.py            41      0   100%
fusers-crud/tests/test_auth.py           30      0   100%
fusers-crud/tests/test_tools.py           5      0   100%
fusers-crud/tests/test_users.py          34      0   100%
fusers-crud/tools/__init__.py             0      0   100%
fusers-crud/tools/app_function.py        15      0   100%
fusers-crud/tools/jwt_token.py           19      0   100%
fusers-crud/tools/passwords.py            5      0   100%
fusers-crud/tools/send_mail.py           12      0   100%
fusers-crud/views/__init__.py             0      0   100%
fusers-crud/views/auth.py                63      0   100%
fusers-crud/views/users.py               49      0   100%
---------------------------------------------------------
TOTAL                                   509      0   100%
```


Local required
 - docker
 - docker-compose
 - pipenv
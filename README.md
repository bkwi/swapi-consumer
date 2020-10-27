## Local setup

```sh
pip install -r requirements.txt
mkdir collections
python manage.py migrate
python manage.py runserver
```

Or if you're hosting SWAPI yourself:

```sh
SWAPI_HOST="http://localhost:5000" python manage.py runserver
```

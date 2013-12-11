# buckstats #

Contains the API code.

# frontend #

Contains the front-end code. All of it is statically-served content.

# Installation #

mkvirtualenv buckstats
pip install -r requirements.txt

Deployment

* sudo apt-get install python-dev supervisor virtualenvwrapper postgresql-server-dev-9.1
* rename stand.py -> main.py
* Compile coffee files
* Separate static files from the python code in production (use nginx conf)
* sudo mkdir /usr/share/nginx/www/data.buckryan.com
*   ^ chown -R buck:buck /usr/share/nginx/www/data.buckryan.com # chown the above
* mkvirtualenv buckstats
*   > deploy into ~/.virtualenvs/buckstats/lib/python2.7/site-packages/
*   -> will put buckstats on the path

# structure #

/usr/share/nginx/www/data.buckryan.com -- static content
~/.virtualenvs -- virtualenv (use virtualenvwrapper)
/etc/nginx/sites-available/ -- data.buckryan.com
/etc/supervisor/conf.d/stand -- supervisor configuration

# uwsgi #

from http://flaviusim.com/blog/Deploying-Flask-with-nginx-uWSGI-and-Supervisor/ #

```
uwsgi -s /tmp/uwsgi.sock -w main:app -H .venv/ --chmod-socket=666
```

# TODO #

* consider using system packages for things like psycopg2 (ie. large libraries
  or libraries that already depend on a system package)

virtualenv --system-site-packages .venv

Deployment

* sudo apt-get install python-dev supervisor
* rename stand.py -> main.py
* Compile coffee files
* Separate static files from the python code in production (use nginx conf)

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

all:

# TODO convert to fabric script

deploy-nginx:
	scp deploy/nginx.conf root@buckryan.com:/etc/nginx/sites-available/data.buckryan.com
	ssh root@buckryan.com "service nginx restart"

deploy-supervisor:
	scp deploy/supervisor.conf root@buckryan.com:/etc/supervisor/conf.d/uwsgi.conf
	ssh root@buckryan.com "service supervisor stop; service supervisor start"

deploy-frontend:
	coffee -co frontend/.compiled-js/ frontend/coffee/
	rsync --recursive --compress --delete -v frontend/ buck@buckryan.com:/usr/share/nginx/www/data.buckryan.com

deploy-buckstats:
	scp requirements.txt buck@buckryan.com:~/
	ssh buck@buckryan.com ".virtualenvs/buckstats/bin/pip install -r requirements.txt"
	rsync --recursive --compress --delete -v \
		buckstats/ \
		buck@buckryan.com:~/.virtualenvs/buckstats/lib/python2.7/site-packages/buckstats

.PHONY: all deploy-nginx deploy-frontend

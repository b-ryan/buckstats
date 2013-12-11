all:

# TODO convert to fabric script

deploy-nginx:
	scp deploy/nginx.conf root@buckryan.com:/etc/nginx/sites-available/data.buckryan.com
	ssh root@buckryan.com "service nginx restart"

deploy-frontend:
	coffee -co frontend/.compiled-js/ frontend/coffee/
	rsync --recursive --compress --delete -v frontend/ root@buckryan.com:/usr/share/nginx/www/data.buckryan.com

.PHONY: all deploy-nginx deploy-frontend

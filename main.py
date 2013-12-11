#!/usr/bin/env python
from buckstats.app import app
import buckstats.routes

def develop():
    app.static_folder = '../frontend'
    static_url_path = '/static'

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    app.run(debug=True)

if __name__ == '__main__':
    develop()

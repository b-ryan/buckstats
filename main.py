#!/usr/bin/env python
from buckstats.app import app
import buckstats.routes

def develop():

    # In development mode, we serve static files with flask. This is not the
    # case in production, where nginx is used. In order to not set up a route
    # for static content in the buckstats.app module, we do it here. But
    # flask doesn't play very nice with manually specifying a static route
    # *after* the app has been created. So we make a route that essentially
    # does the same thing as flask's static route.
    app.static_folder = '../frontend'

    @app.route('/', defaults={'filename': 'index.html'})
    @app.route('/<path:filename>')
    def static(filename):
        return app.send_static_file(filename)

    # @app.route('/<path:filename>')
    # def static_files(filename):
    #     print filename
    #     return app.send_static_file(filename)

    app.run(debug=True)

if __name__ == '__main__':
    develop()

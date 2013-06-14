#!/usr/bin/env python
import bottle

@bottle.get('/')
def index():
    return "hello world!"

bottle.run(port=8080)

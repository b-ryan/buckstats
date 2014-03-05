from fabric.api import (
    local, run, put, cd
)

def pack():
    local('./setup.py clean sdist', capture=True)

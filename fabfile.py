import os

from fabric.api import env, run, put, local, cd, sudo
from fabric.contrib.files import exists

env.hosts = ['loogica.net']
env.user = 'deploy'

config = {}

config['name'] = 'news.loogica.net'
config['repo'] = 'https://github.com/loogica/news.loogica.net.git'
config['apps_path'] = '/opt/apps/'
config['path'] = os.path.join(config['apps_path'], config['name'])

def send_settings():
    put('settings.ini', config['path'])
    put('nginx.vhost', config['path'])
    put('uwsgi.conf', config['path'])

def create_app_dir():
    with cd(config['apps_path']):
        run('git clone {repo}'.format(**config))

def check_app():
    app_path = exists(config['path'])
    if not app_path:
        create_app_dir()
    assert exists(config['path'])

def setup_webapp():
    check_app()
    with cd('/etc/nginx/sites-enabled'):
        sudo('ln -s {path}/nginx.vhost urlsh.vhost'.format(**config))
    with cd('/etc/supervisor/conf.d'):
        sudo('ln -s {path}/uwsgi.conf urlsh.conf'.format(**config))

def update_webapp():
    with cd(config['path']):
        run('git pull origin master')

    sudo('supervisorctl reload')
    sudo('service nginx stop')
    sudo('killall nginx')
    sudo('service nginx start')

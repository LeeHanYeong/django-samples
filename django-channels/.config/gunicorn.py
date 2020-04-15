daemon = False
chdir = '/srv/channels'
bind = '0.0.0.0:8000'
workers = 2
threads = 1
timeout = 60
accesslog = '/var/log/gunicorn.log'
errorlog = '/var/log/gunicorn-error.log'
capture_output = True
raw_env = [
    'DJANGO_SETTINGS_MODULE=config.settings',
]

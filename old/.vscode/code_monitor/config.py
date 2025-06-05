import multiprocessing

bind = "0.0.0.0:9108"
proc_name = "code_exporter_api"
workers = 1
threads = workers * 4
loglevel = "debug"
daemon = False
backlog = 512
debug = False
timeout = 180
pidfile = "gunicorn.pid"
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = "-" 
errorlog = "-"
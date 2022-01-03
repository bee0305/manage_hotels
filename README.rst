#Cron get_api every 1 minute
$sudo crontab -e
*/1 * * * * + command (see below)

# for wsl2 (seems systemd does not boot on wsl2)|=>
$ sudo /etc/init.d/cron start
 * Starting periodic command scheduler cron                                                                      [ OK ]
(venv) ...:~/dj/travel/city$ service --status-all
 [ - ]  apparmor
 [ + ]  cron

# check (current)
*/1 *  *    *   *    '/home/tanja/dj/travel/city/city/cron/get_api.sh'

chmod +x /home/tanja/dj/travel/city/city/cron/get_api.sh
 # check
 bash -c '/home/tanja/dj/venv/bin/python manage.py get_api'

# commands wsl2

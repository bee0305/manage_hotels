#Cron get_api every 1 minute
$sudo crontab -e
*/1 * * * *  path-to-sh-file 


$ sudo /etc/init.d/cron start
 * Starting periodic command scheduler cron                                                                      [ OK ]
$ service --status-all 
 [ + ]  cron

# check (current)
$chmod a+x get_city.sh
$chmod a+x get_hotel.sh
$./get_city.sh
$./get_hotel.sh

#
*/1 *  *    *   *    /home/..../city/city/cron/get_hotel.sh

 


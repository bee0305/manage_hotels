Cron 
======
Management commands: 
------------------
* get_city
* get_hotel

*/1 *  *    *   *    /home/..../city/city/cron/get_hotel.sh >> /home/.../logs/city.log
---------------------------------------------------------------------------------------


Help info:
----------
``-`` $ sudo /etc/init.d/cron start
``-`` $sudo crontab -e
``-`` */1 * * * *  path-to-sh-file 


Starting periodic command scheduler cron                                                                      
----------------------------------------
``-`` $ service --status-all 
 [ + ]  cron

Check
------
``-`` $chmod a+x get_city.sh
``-`` $chmod a+x get_hotel.sh





 


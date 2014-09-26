---
layout: post
title:  "Auto-provisioning ST Math Rosters with KIPP Silo"
date:   2014-09-25 17:00:00
flag:   tutorial, st_math, integration
---

This is some quick and dirty documentation for auto-provisioning rosters to ST Math from your KIPP Silo instance.

I've committed to [our github page](http://www.github.com/kippdata/silo) [two](https://github.com/kippdata/silo/blob/master/scripts/Ed_Tech_Integrations/ST_Math/ST_Math_Rosters.py) [Python](https://github.com/kippdata/silo/blob/master/scripts/Ed_Tech_Integrations/ST_Math/ST_Math_Teacher_Rosters.py) scripts, and a [config file](https://github.com/kippdata/silo/blob/master/scripts/Ed_Tech_Integrations/ST_Math/ST_Math.config), 

For this roster provision to work you need to have a [KIPP Silo instance up and running]({% post_url 2014-08-02-SQL-Server-on-AWS %}) and have [linked it to PowerSchool]({% post_url 2014-09-16-Setting_Up_PoweSchool_on_SQL_Server %}) (if you are using a different SIS then you'll need to change the SQL statements in both scripts to pull in the same field from that SIS.  If  you do that, then please share you work with KIPP Silo project os other regions and schools don't needlessly repeat your excellent work).

You simply need to save those files and create a directory named `/data` (this is where the your students and teachers data will be saved before being shipped off to ST Math via SFTP) somewhere (at KIPP Chicago we have it at `C:\robots\ST_Math\`) and then update the `ST_Math.config` file with your KIPP Silo credentials and your ST Math SFTP credentials (if you don't have ST Math SFTP credentials, just ask your ST Math rep).  Here is the entirety of the config file:

{% highlight powershell %}
[Silo]
uid: your_silo_username
pwd: your_silo_password
server: 127.0.0.1
port: 1433
condition: grade_level NOT IN (3,4)

[STMathSFTP]
host: sftp.stmath.com
password: your_stmath_sftp_password
username: your_stmath_sftp_username
{% endhighlight %}

You simply substitute your own credentials.  You might want to check that your are using the same local IP address and port number, but those are standard for SQL Server.

Now, the `condition:` argument is important.  If you put in (unquoted) Oracle SQL that is legal for a `WHERE` clause, then the script will subset your data accordingly.  In the example here all  currently enrolled students in grades 3 and 4 would be excluded. If you want to include every enrolled student then simply delete everything to the right of the colon (err, prompt?).  Do leave the `condition:` part though: otherwise you'll break the `ST_Math_Rosters.py` script. 

You then need to [set up a Task Scheduler job](http://technet.microsoft.com/en-us/library/cc766428.aspx) that runs both the `ST_Math_Rosters.py` file and the `ST_Math_Teacher_Rosters.py` file.  The job can run as frequenlty as you like: once a week, once a day, once an hour.   

That's it!  

If you've setup the config file correctly the scripts will hit your KIPP Silo database and through it your PowerSchool Instance to pull your current enrollment and homeroom teachers from PowerSchool.  The scripts will clean up the data, add some necessary columns, create relationships between teachers and students and save the two rosters as CSVs in the data directory.  The scripts will then connect to ST Math's SFTP server and send the files over.  ST Math then updates your rosters.  We run this scripts hourly since ST Math checks the directory you sent the files to hourly.

That's really it!

Stay tuned for pulling your data out of ST Math and loading it into KIPP Silo. (A feat I will achieve by stealing KIPP NJ's extant scripts and do some light refactoring to make them more configurable!) 
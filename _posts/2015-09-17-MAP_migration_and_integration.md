---
layout: post
title:  "Alumni (SalesForce) DB Integration"
date:   2015-09-17 12:00:00
flag:   tutorial, nwea map, integration
---
I’ve added the  python script we use to grab a CDF from NWEA and load into our database.  

I’ve also added a sql script we used to migrate from the old CDF format to the new CDF format (NB that the script triggers a SQL Server Agent Job that you have to define that in turn triggers a stored procedure that reads the CSVs and upserts into the db).

Here’s [the link](https://github.com/kippdata/silo/tree/master/scripts/Ed_Tech_Integrations/NWEA_MAP).

Let me know if you have questions. (and again thanks to @cbini for saving me a days worth of work).


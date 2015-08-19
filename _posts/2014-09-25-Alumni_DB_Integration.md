---
layout: post
title:  "Alumni (SalesForce) DB Integration"
date:   2015-08-19 12:00:00
flag:   tutorial, salesforce, alumni_db, integration
---

This project is still alive, in case you all were wondering.  I've worked with Charlie Bini and Andrew MArtin at KIPP NJ and we've created a very nice script that grabs the five most important Alumni DB tables form sales force and loads them up to a SQL Server DB.  They are up on our [our github page](http://www.github.com/kippdata/silo) now.  You can find them [here](https://github.com/kippdata/silo/tree/master/scripts/Alumni_mirror)! 

You'll find three files in that repo.  You only need to make changes in `config.py` which has fields for your Salesforce credentials and your. It looks like this: 

{% highlight python %}
## Alumni Salesforce DB configurables
SF_UID = 'you@kipphawaii.org'
SF_PWD = 'secret_wd!'
SF_TOKEN =  'very_long_token_from_salesforce'

## Silo DB configurables
DB_TYPE = 'mssql'
DB_API = 'pyodbc'
DB_DNS_NAME = 'Silo_Alumni_64'
DB_SERVER = ''
DB_NAME = 'Alumni_mirror'
DB_USERNAME = ''
DB_PASSWORD = ''
{% endhighlight %}

You simply substitute your own credentials.  Easiest use is to set up a DNS directly to where in SQL Server instance you'll store these data.

The other two files are `databaseconfig.py` and `sf_get_and_load.py`.  The first one is a module that is imported into the second and has some resuable functions that can be used to connect to SQL Server as well as  push data from a `pandas dataframe` up to SQL server.  It creates a new table if that data is new; otherwise it trunctes the table and appends you data.  Not as sophisticated as an upsert, but for most integrations good enough.  

The `sf_get_and_load.py` is were the magic happens. It pulls five tables from the Alumni DB, creates dataframes for each, and then loads each up to SQL server.  The five tables are:

* `Account`, 
* `Contact`, 
* `College_Persistence__c`, 
* `Contact`, 
* `Contact_Note__c`, 
* `Enrollment__c`.

You can [set up a Task Scheduler job](http://technet.microsoft.com/en-us/library/cc766428.aspx) to hit the `sf_get_and_load.py`.  You will in all likelihood need to use a 64-bit Python interpretor, since the `Account` table in the Alumni DB is huge and the `pandas` package won't be able to handle it in 32-bit Python. The (Anaconda distribtuion is great)[https://store.continuum.io/cshop/anaconda/].


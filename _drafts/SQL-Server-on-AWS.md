---
layout: post
title:  "Setting up SQL Server on AWS"
date:   2014-07-30 14:15:00
---

This step-by-step tutorial covers the process for launching your own version of the KIPP Silo data warehouse on [Amazon Web Services](http://aws.amazon.com).  It will cover how to launch an EC2 instance with Windows Server as your operating system and SQL Server as the database that will serve as your KIPP Silo data warehouse. **Note that these instructions are good for the day they were written.  If you are reading them sometime down the road they might not accurately reflect your current state of the world/SQL Server/Windows Server/AWS/etc.**

## Amazon Web Services

First, you'll need to go to [Amazon Web Services](http://aws.amazon.com/) and click on sign up:

![AWS Landing Page]({{ site.baseurl }}/images/1-AWS_Sign_up_1.png "AWS Landing Page")

Go throught the sign up process and then you will find your self at the **AWS Managment Console**. This is where you will launch an EC2 instance, which is to say am **E**lastic **C**ompute web server hosted and maintained by your favorite purveyour of books and dry goods. But don't worry, they are crack experts at hosting stuff for you in *The Cloud*.

You will see a bunch of color coded  and coordinated icons for different AWS services. The second one in organge on the left says EC2.  That's the one you want.  Click it!

![AWS Management Console 1]({{ site.baseurl }}/images/2-AWS_Console_1.png "AWS Management Console 1")

This brings your the **EC2 Dasboard**. This is were you managage all your different EC2 instances.  If this is your fist time launching an EC2 instance, then you'll see lots of zeros and not much of any thing else.  

To orient you to the console you'll see that as of this writing KIPP Chicago has two running instances under the **Resources** section.  They both support our data analysis and interactive reporting website: one instance is pretty powerful machine that we use for production and the other is the development server.  There is an IP address for each and each has its own storage.  And we have one key pair, which is how we securaly access these machines (at least the first time we do so).

The importand part of this screen for this step-by-step is the big blue button under the **Create Instance*** section in the center panel labeled **Launch Instance**.  Go ahead and click that bad boy:

![AWS EC2 Dashboard]({{ site.baseurl }}/images/3-AWS_Launch_Instance.png "AWS EC2 Dashboard")


### Choose AMI
This is the screen where you will need to pick the [Amazon Machine Image](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) for the operating system (Microsoft Windows Server 2012 R2) already loaded with your copy of fully licensed database (SQL Server Standard).  You'll need to scroll down the page a bit to find the AMI you want: 

* Microsoft Windows Server 2012 R2 with SQL Server Standard - ami-82e023ea

![AWS EC2 Dashboard]({{ site.baseurl }}/images/4-Choose_AMI.png "AWS EC2 Dashboard")


### Choose Instance Type

Here you pick your server size, configuration, and type.  The cheapest you can buy from an on-demand instance (i.e., a pay-as-you-go plan) is m3.medium that runs you $0.35.  You can drop that price seven fold to $0.05 by paying a little bit upfront ($172) for a longer committment (3-years). That's only about $1,500 over three years (i.e., $500/year) to have your Silo data warehouse hosted in the cloud.







## I'm scared, what should I do?
You want to select a micro instance with SLQ Server Express (Free usage tier).  

It's a playground.  Fall down, get back up, no real risks. Then go below 

## Ok, so what do I loose by going the micro instance/SQL Server Express route?

Spin up an EC2 instance with Windows Server 2012 and SQL Server Standard
Why?  Because you get **Agent**, which allows you to run timed tasks (i.e, you finally get a robot to do your building).








---
layout: post
title:  "Setting up SQL Server on AWS"
date:   2014-08-02 20:00:00
flag:   tutorial
---

This step-by-step tutorial covers the process for launching your own version of the KIPP Silo data warehouse on [Amazon Web Services](http://aws.amazon.com).  *Note: I've never done this before. Like ever.* In other words this is my first time doing this ever and I'm documenting here so that (i) big KIPPsters that haven't done this before can see how it can be done and (ii) any mistakes I make are documented and someone---anyone---can correct them.


It will cover how to launch an EC2 instance with Windows Server as your operating system and SQL Server as the database that will serve as your KIPP Silo data warehouse. **Note that these instructions are good for the day they were written.  If you are reading them sometime down the road they might not accurately reflect your current state of the world/SQL Server/Windows Server/AWS/etc.**

_**Table of Contents**_

* TOC
{:toc}

## Amazon Web Services

First, you'll need to go to [Amazon Web Services](http://aws.amazon.com/) and click on sign up:

![AWS Landing Page]({{ site.baseurl }}/images/1-AWS_Sign_up_1.png "AWS Landing Page")

Go through the sign up process and then you will find your self at the **AWS Managment Console**. This is where you will launch an EC2 instance, which is to say an **E**lastic **C**ompute web server hosted and maintained by your favorite purveyor of books and dry goods. But don't worry, they are crack experts at hosting stuff for you in *The Cloud*.

You will see a bunch of color coded  and coordinated icons for different AWS services. The second one in orange on the left says EC2.  That's the one you want.  Click it!

![AWS Management Console 1]({{ site.baseurl }}/images/2-AWS_Console_1.png "AWS Management Console 1")

This brings your the **EC2 Dashboard**. This is were you manage all your different EC2 instances.  If this is your first time launching an EC2 instance, then you'll see lots of zeros and not much of any thing else.  

To orient you to the console you'll see that as of this writing KIPP Chicago has two running instances under the **Resources** section.  They both support our data analysis and interactive reporting website: one instance is relatively powerful machine that we use for production and the other is the development server.  There is an IP address for each and each has its own storage.  And we have one key pair, which is how we securely access these machines (at least the first time we do so).

The important part of this screen for this step-by-step is the big blue button under the **Create Instance*** section in the center panel labeled **Launch Instance**.  Go ahead and click that bad boy:

![AWS EC2 Dashboard]({{ site.baseurl }}/images/3-AWS_Launch_Instance.png "AWS EC2 Dashboard")


### Choose AMI
This is the screen where you will need to pick the [Amazon Machine Image](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) for the operating system (Microsoft Windows Server 2012 R2) already loaded with your copy of fully licensed database (SQL Server Standard).  You'll need to scroll down the page a bit to find the AMI you want: 

* Microsoft Windows Server 2012 R2 with SQL Server Standard - ami-82e023ea

![AWS Choose Instance]({{ site.baseurl }}/images/4-Choose_AMI.png "AWS Choose Instance")


### Choose Instance Type

Here you pick your server size, configuration, and type.  The cheapest you can buy from the on-demand instances (i.e., a pay-as-you-go plan) is the m3.medium that runs you $0.36/hour.  You can drop that price in half to $0.16/hour by paying a little bit upfront ($1061) for a longer commitment (3-years). That's only about $5,300 over three years (i.e., $1,764/year) to have your Silo data warehouse hosted in the cloud.  Not to shabby given what your region is paying to ed tech companies to ***REMOVED*** all of your data (ha! See what I did there).

So choose the m3.medium instance and click the **Next: Configure Instance Details** button
![AWS Choose Instance]({{ site.baseurl }}/images/5-Choose_Instance.png "AWS Choose Instance")

### Configure Instance Details
This will be quick and easy.  You don't need to change anything if you don't want to.  For the sake of safety, though, I like to check the **Protect against accidental termination** box.  Why?  Well terminating and instance kills it forever. In lieu of terminating an instance, we can stop the instance, which saves the state of the instance and shuts down the server (which can save you money).  You can always restart a stopped instance, but terminated instances are gone forever. Whether you check that box or not, go ahead and click **6. Configure Security Group** on the breadcrumb trail at the top of the page. (I'm skipping **Add Storage** and **Tag Instance**.  You can continue through those steps if you want, as they are pretty self-explanatory, but the default storage should be sufficient and tags are cool but not necessary.)

![AWS Configure Instance]({{ site.baseurl }}/images/6-Configure_Instance.png "AWS Configure Instance")

### Configure Security Group

Here you can either create a new security group, which is essentially a set of rules for a firewall that secures which protocols, ports, and IP addresses will be able to access your Windows Server.  The out of the box set-up should be sufficient for right now.  You can rename the Security Group name to something memorable (how about KIPP Silo!).  The click **Review and Launch**. 

![AWS Configure Security Group]({{ site.baseurl }}/images/7-Config_Security_Group.png "AWS Configure Security Group")


### Launch Instance!

You'll now be at the review and launch instance page.  Sweet!

![AWS Launch]({{ site.baseurl }}/images/8-Launch.png "AWS Launch")



### Key Pair
Before you launch completely, you'll need to assign a **key pair** to the server.  The key pair works just like keys do to your home or car.  You must have possession of a special file (a key file) to access the server.  Without the key you can't access the server initially.  Upon clicking "Launch" you should see a pop-up dialogue where you can either select an existing key pair if you already have or create a new key pair (AWS has one side of the key pair---called the public key---and you have the other side--called the private key or PEM file).  Here I create a new key pair and name it **KIPP Silo**. You'll download the key to your desktop/laptop, so please keep track of it and save it somewhere memorable. 

![AWS Key Pair]({{ site.baseurl }}/images/9-Key_Pair.png "AWS Key Pair")


### Connect

Click on this link and follow the instructions provided to connect to the instance. AWS provides clear instructions on connecting to your instance for Windows, Mac, or Linux.
![AWS Connect]({{ site.baseurl }}/images/10-AWS_Connect_to_Windows_Instance.png "AWS Connect")

And that is it.  You now have a server up and running with a database installed to boot. 

## This seems a all a bit overwhelming and maybe even a little scary, what should I do?

1. Remember, that I've never done this before too, so it was a little scary for me.  But I still go it done.  AWS is super nice to the new user and provides plenty of attention.
2. You can call/email/text me or Andrew or James or many other folks throughout the network.
3. Do all of the above but in no risk format.  You want to select an AMI running Windows Server with SQL Server Express on a micro instance.  This set up, when used with a new account, is in the so called "Free usage tier", meaning you have a year to use a very small instance with the lower powerd database **FOR FREE**.

It's a playground.  Fall down, get back up, no real risks. When you are comfortable, then follow these instructions for the SQL Server Standard edition.

## Next Steps
In my next couple of posts, I'll demonstrate how to launch in database instance (this will be your copy of KIPP Silo), how to set-up a persistent VPN connection to a Pearson-hosted PowerSchool instance, how to link your PowerSchool instance to the KIPP Silo SQL Server database, and how to link your Illuminate instance to your KIPP Silo SQL Server database.  

Stay tuned!!!









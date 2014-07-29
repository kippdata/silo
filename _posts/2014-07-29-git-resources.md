---
layout: post
title:  "GitHub and Git Tutorials"
date:   2014-07-29 06:19:13
---
So I promised everyone new to distributed development projects a tutorial of sorts on [GitHub](http://www.GitHub.com) and its underlying version control system [Git](http://Git-scm.com). Rather than writing a super long tutorial and in the spirit of "not reinventing the wheel", I hope dear readers you'll forgive me for creating this **Resource Roundup**.  And rather than be a brain dump of links, this roundup will be curated and sectioned so your can jump in where you feel most comfortable.


##What are Git and GitHub, anyhow?


###GitHub
GitHub at its core is a social networking site, not unlike [Facebook](https://wwww.facebook.com) or even [KIPP Share](http://www.kippshare.org). You have a profile, follow folks, and can even post stuff. The stuff you post, however, is where GitHub differs from traditional social networking sites. You (usually, but not exclusively) post the code and documents of the projects you are working on the site. So *de minimus*, GitHub gives you a secondary storage place (the first is likley your laptop) for all of your work. You can save any type of file there, not just lines of code. And having a second copy of your work is really awesome when you computer blows up or you somehow write over [that awesome data flow diagram you were putting together for KSS]({{ site.baseurl }}/images/Data_system_diagram.svg "KIPP Chicago Data Systems")(this happended to me!).


Nevertheless, GitHub really shines at hosting code repositories and supporting software development.  At the heart of its support is the Git [version control](http://Git-scm.com/video/what-is-version-control) system.  And GitHub makes Git super easy to use by providing a visual user interface and a place to host your repositories (the set-up of which is a snap and really well documented).  Of course, you can always use GitHub from the command line.

###Git
Git is version control software, which means it manages changes to a project without overwriting any part of that project.  Saving everything you've ever done means that (i) you can always revert to an earlier version of anything you are working on if you aren't pleased with your progress and (ii) you can work through changes made by other people, say Andrew Martin and myself, *on the same document*!  Git will save my version, Andrew's version, the version we both started working from, and provides and interface to identify differences between the three documents and merge them together into one new document. It's a bit like [Word's Track Changes](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0CCsQFjAB&url=http%3A%2F%2Foffice.microsoft.com%2Fen-us%2Fword-help%2Ftrack-changes-while-you-edit-HA001218690.aspx&ei=X4DXU8SoIvHO8QGd_oCYDg&usg=AFQjCNEoPwfzhJ8KMQ4nP5gEdQ4KRtCxEQ&sig2=OyBmNiL6lUojR1el2DtnHQ&bvm=bv.71778758,d.b2U) feature but you always have every copy of every version everyone ever put together without having to save a zillion files with different names (and naming conventions when working with others).

So in the end, using Git and GitHub gives you a system for backing-up, version controlling, and collaboratively sharing your work.

(Awseome fun Git fact for nerds: you have the inventor or [Linux](http://www.linux.com/) to thank for Git: [Linus Torvalds](http://en.wikipedia.org/wiki/Linus_Torvalds)!)

##OK, backing-up, version controlling, and sharing my code seems the honorable thing to do.  How do I get started?

Great! Here are some tutorials/resources with my comments:

###Tutorials

* [GitHub For Beginners: Don't Get Scared, Get Started](http://readwrite.com/2013/09/30/understanding-github-a-journey-for-beginners-part-1). A super gentle introduction to both Git and Github from a non-programmers point of view. Includes some motivation (borrowed heavily from in the sections above), a glossary, and a tutorial on how to set up Git and GitHub **for the first time**. Highly recommended.
* [GitHub For Beginners: Commit, Push And Go](http://readwrite.com/2013/10/02/github-for-beginners-part-2). This is the second installment to the link above. Shows you how to add new files to your repository, save versions to your local repository (commit them), and save versions to your web-based GitHub repository (push them). Again, this is a very gentle introduction.
* [How the Heck Do I Use GitHub?](http://lifehacker.com/5983680/how-the-heck-do-i-use-github). From [Lifehacker](http://www.lifehacker.com), similar to the above, only shorter.
* [Git Tutorials](https://www.atlassian.com/git/tutorial). From basics too more sophisticated help on things like changing your repositories past history (perhaps you accidently saved a password in the clear to a commit).

### Other Resources
* [Tru Git](https://try.github.io/levels/1/challenges/1).  Read through some or all of the above, but still feeling some trepidation? No problem.  Speng 15 minutes on Try Git to get a sense of how this all works! (And Try Git's code is hosted on ... GitHub!)
* [Git Workflows](https://www.atlassian.com/git/workflows).  This is an intermediate tutorial and discussion of various Git "workflows".  Workflows describe rules and timing around how you pull code from a repository and push it back up when you are done working on it with a group of people.  There are probably an infinite number of ways teams of developers could use to coordinate development.  These are the most common. The most important tuturial to read is the one on [feature-branch workflows](https://www.atlassian.com/git/workflows#!workflow-feature-branch), since that is teh workflow we will employ for KIPP Silo.
* [git - the simple guide](git - the simple guide). An excellent cheat sheet. "no deep shit ;)"
* [Git Cheatsheet](https://www.atlassian.com/dms/wac/images/landing/git/atlassian_git_cheatsheet.pdf). A two page pdf cheatsheet.
* [Interactive Git Cheatsheet](http://ndpsoftware.com/git-cheatsheet.html#loc=workspace;).  It is what it says it is.
* [Escape a Git mess: Step-by-step](http://justinhileman.info/article/git-pretty/git-pretty.png). What it says it is, too, and somewhat tongue-in-cheek.

Feel free to let me know if you have any questions or I've left anything out of this round-up!



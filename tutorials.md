---
layout: page
title: Tutorials
permalink: /tutorials/
---

## Setting up a Silo data warehouse

 <ul>
  {% for post in site.posts %}
  	{% if post.flag == 'tutorial' %}
    <li>
      <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a>
    </li>
    {% endif %}
  {% endfor %}
</ul>
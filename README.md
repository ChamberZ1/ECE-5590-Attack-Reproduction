# ECE-5590-Attack-Reproduction

Objective: Malicious code in websites

Part 1: Build a simple dummy social networking site and use it to demonstrate SQL injection Links to an external site., XSS Links to an external site., and CSRF Links to an external site. vulnerabilities.

Part 2: Construct an XSS worm Links to an external site. to attack your site, like the Samy worm Links to an external site. that infected MySpace.

Part 3: Implement defenses against each threat. Bonus challenge: Discover an undocumented XSS vulnerability in a popular website.



## Steps


# Setup DB

```
python setup_db.py
```


# Start Website

```
python app.py
```


# SQL injection

Register a user with the following
    - Username: admin
    - Password: password of your liking

Log in with these credetials

Logout

Go back to login page as type the following into username:
    - Username: admin' --
    - Password: anything doesnt matter

This logs you in as admin without needing the password


# XSS

Login as any users

Create a post with the following:
    - <script>alert('XSS Attack!');</script>

Go to global feed and see the alert


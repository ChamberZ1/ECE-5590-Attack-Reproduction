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
The site comes with 3 accounts with the following credentials:

- `admin:admin`
- `bob:bob`
- `alice:alice`

Additional accounts can be created

Register a user with the following
- Username: >username<
- Password: >password<

Log in with these credentials

# SQL injection

Go to login page and append `' --` to the username, for example:
- Username: `admin' --`
- Password: >any<

This logs you in as admin without needing the password


# XSS

Login as any users

Create a post with the following:
    - <script>alert('XSS Attack!');</script>

Go to global feed and see the alert


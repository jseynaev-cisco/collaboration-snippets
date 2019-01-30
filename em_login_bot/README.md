# em-login-bot

Cisco Webex Teams bot that can log a user in with UCM Extension Mobility 
Feature. See https://teams.webex.com/ to check out what Cisco Spark is, 
then see https://developer.webex.com/ on bots

Just say "log me in into [number on the phone]" and the bot will do it's best to do so.
When you are done for the day, just say "log me out" ...

### disclaimer
EM Login BOT is a Proof of Concept, provided 'as is' without support. 
Suggestions or questions can be left here in the comments, but will not be 
monitored regularly.

## versions
**v0.1**

Proof of Concept, it works ... most of the time. It also gives some useful 
errors back ... most of the time

## commands
- hello
- log me in into [number on the phone]
- log me out
- help

## limitation
- Uses your primary profile only (cannot choose profile yet)
- No EMCC
- not handling multiple logins (if enabled on ucm)

## How to run
First of all, make sure you have a bot for Cisco Spark 
(https://developer.webex.com/) and AXL and Extension Mobility are enabled 
on your UCM Clusters  
The code uses [Flask](http://flask.pocoo.org/) to run a webserver 
listening for POST requests on the root URI (/), you will need a URL 
that is www reachable (or use something like ngrok to tunnel)

To run the BOT/server, clone this repo and rename config.sample.py to 
config.py. Edit config.py to get all the passwords and creds suiting 
your environment.  
Then run `$python em_login_bot.py` to run the Flask webserver 
(it will listen on port 1555 if you don't change the code), if you want it a 
bit more production ready, try running with gunicorn:  
`$gunicorn -b 0.0.0.0:1555 --log-level debug --log-file /some/patch/to/bot.log -D em_login_bot:app`  

That should be it, have fun!

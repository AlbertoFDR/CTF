# Bookmarks

## Author 

bubu

## Category

web

## Difficulty

hard 

## Description

I'm creating a bookmark site for my friends, do you like it? Feel free to test it out!

## Attachment

Attachments: `bookmarks.tar.gz`

## Deployment Notes

Challenge has two containers: `web`, and `bot`.

## Bot Logic

Bot will visit the attacker url and then, register and login with FLAG as username. 

## Solution
### Header injection and CSRF attack

For solution. First using the header injection in the username ([ref](https://github.com/pallets/flask/issues/4238)) to push the CSP as content and not as header, making the XSS also possible. Then, the idea is to use this XSS with a CSRF attack and then open a new tab with `window.open` (Tab2), and while the first tab (Tab1) is used by the bot to register/login, from `Tab 2` we can open `/dashboard` and get the flag.

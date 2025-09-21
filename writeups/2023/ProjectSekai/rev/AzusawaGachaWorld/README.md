## Azusawa’s Gacha World (250 Solves)
## Author: Iyed
### Not solved during CTF

[Official writeup](https://enscribe.dev/blog/sekaictf-2023/azusawas-gacha-world/)

This particular challenge involves a gacha game that has been crafted using Unity. It's worth giving credit to the author for the remarkable development effort put into creating a gacha game for a CTF challenge.

The solution to this CTF can be uncovered using the dnSpy tool. In the case of Linux (which is my scenario), I utilized the environment values of 'http_proxy' to capture all the communication between the game and the server. Finally, we just need to replicate the POST changing the number of pulls to get a rarity 4 character (a.k.a the flag).

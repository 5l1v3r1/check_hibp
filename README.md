![alt text](http://leonvoerman.nl/coding/hibp.png)

# hibp.py
Check haveibeenpwned for account breaches with a list of usernames

Shows breached or not, date of breach and where you got breached.

Example:
```Shell
python hibp.py -f ~/Documents/emails.txt -s ~/Documents/result.txt -b 2
```

Base Code:
```Python
check = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/%s' % account)
```

```Python
if check.status_code == 200:
   return ('%s \033[31m[BREACHED]\033[0m %s -> %s -> %s') % (account.ljust(50), breachdate.rjust(15), latestbreach, breachedon)
```

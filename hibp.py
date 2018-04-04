#!/usr/bin/python
import sys, requests, argparse, time

if len (sys.argv) < 2:
    print('\033[31m[ERROR]\033[0m Please, provide a list'); sys.exit(1)
else:
    pass

def parse_args():
    #Create the arguments
    parser = argparse.ArgumentParser(description='Check accounts on haveibeenpwned.com')

    parser.add_argument("-f", "--file", help="Location to a list with account names or Email addresses. Example: -f ~/Documents/accounts.txt")
    parser.add_argument("-s", "--save", help="Save results to a file. Example: -s ~/Documents/result.txt")
    parser.add_argument("-b", "--burst", help="Set sleep time. Sleep time of 0 can trigger Cloudflare protection and/or false positive results.")
    #parser.add_argument("-d", "--date", help="Set min/max. Show first or latest breach. Default: max")

    return parser.parse_args()

args = parse_args()

try:
    accounts = open(args.file).readlines()
except IOError:
    print('\033[31m[ERROR]\033[0m Cannot open this file')


def search(account):
    breachedon = []
    dates = []


    try:
        check = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/%s' % account)
    except KeyboardInterrupt:
        print('Stopped...')

    try:
        for title in check.json():
            breachedon.append(title["Title"].encode('utf-8'))

        #for breachdate in check.json():
        #    breachdate = breachdate["BreachDate"]


        for date in check.json():
        #    breachdate = date["BreachDate"]
            dates.append(date["BreachDate"].encode('utf-8'))
            latestbreach = max(dates) # Latest breach
            breachdate = min(dates) # first breach

    except Exception:
        pass

    # Check status code
    if check.status_code == 404:
        return ('%s \033[32m[NOT FOUND]\033[0m') % account.ljust(50)
    elif check.status_code == 200:
        return ('%s \033[31m[BREACHED]\033[0m %s -> %s -> %s') % (account.ljust(50), breachdate.rjust(15), latestbreach, breachedon)

    elif check.status_code == 503:
        print('\033[31m[ERROR]\033[0m Limit reached, temporarily banned by Cloudflare. Exiting....'); sys.exit(1)
    else:
        return ('%s \033[32m[NOT FOUND]\033[0m') % account.ljust(50)


# Set sleep time
if args.burst == None:
    timer = '1.5'
else:
    timer = float(args.burst)

# Header
header = 'Account'.ljust(50), 'Status'.ljust(15), 'First breach / Latest Breach / Breach'
print('\033[94m{0[0]} {0[1]} {0[2]}\033[0m'.format(header))

# Check accounrs
for l in accounts:
    if args.save == None:
        print(search(l.strip()))
        time.sleep(float(timer))

    else:
        result = search(l.strip())

        with open(args.save, 'a+') as f:
            print(result)
            f.write(result + '\n')
            f.close()

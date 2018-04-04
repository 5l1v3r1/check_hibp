#!/usr/bin/python
import sys, requests, argparse

if len (sys.argv) < 2:
    print('\033[31m[ERROR]\033[0m Please, provide a list'); sys.exit(1)
else:
    pass

def parse_args():
    #Create the arguments
    parser = argparse.ArgumentParser(description='Check accounts on haveibeenpwned.com')

    parser.add_argument("-f",
                        "--file",
                        help="Location to a list with account names or Email addresses. \
                                Example: -f ~/Documents/accounts.txt")
    parser.add_argument("-s", "--save", help="Save results to a file on the given location \
                                Example: ~/Documents/")

    return parser.parse_args()

args = parse_args()

try:
    accounts = open(args.file).readlines()
except IOError:
    print('\033[31m[ERROR]\033[0m Cannot open this file')


def search(account):
    check = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/%s' % account)

    # Check status code
    if check.status_code == 404:
        return ('\033[32m[NOT FOUND]\033[0m \t%s') % account
    elif check.status_code == 400:
        return ('\033[32m[NOT FOUND]\033[0m \t%s') % account
    elif check.status_code == 200:
        return ('\033[31m[BREACHED]\033[0m \t%s') % account
    else:
        return ('\033[32m[NOT FOUND]\033[0m \t%s') % account

# Check accounrs
for l in accounts:
    if args.save == None:
        print(search(l.strip()))
    else:
        result = search(l.strip())

        with open(args.save + 'result.txt', 'a+') as f:
            print(result)
            f.write(result + '\n')
            f.close()

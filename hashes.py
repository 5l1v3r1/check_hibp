#!/usr/bin/python
import requests, hashlib, argparse, time, sys

def parse_args():
    #Create the arguments
    parser = argparse.ArgumentParser(description='Check passwords on haveibeenpwned.com')

    parser.add_argument("-f", "--file", help="Location to a list with hashes or clear-text passwords. Example: -f ~/Documents/passwords.txt")
    parser.add_argument("-s", "--save", help="Save results to a file. Example: -s ~/Documents/result.txt")
    parser.add_argument("-b", "--burst", help="Set sleep time (default: 1.5). Sleep time of 0 can trigger Cloudflare protection and/or false positive results.")
    parser.add_argument("-c", "--check", help="Check a single password or hash")
    parser.add_argument("-p", "--password", help="Hash a clear-text password (MD5, SHA1, SHA-256, SHA-512)")

    return parser.parse_args()

args = parse_args()

if args.password:
    # Print a header
    header = 'Type'.ljust(20), 'Hash'
    print('\033[94m{0[0]} {0[1]}\033[0m'.format(header))

    # Hash it
    print('MD5'.ljust(21) + hashlib.md5(args.password).hexdigest())
    print('SHA-1'.ljust(21) + hashlib.sha1(args.password).hexdigest())
    print('SHA-256'.ljust(21) + hashlib.sha256(args.password).hexdigest())
    print('SHA-512'.ljust(21) + hashlib.sha512(args.password).hexdigest())
    sys.exit(0) # Done


try:
    passwords = open(args.file).readlines() # Open file
except Exception as e:
    if args.check: # if -c option, don't open a file or error
        pass
    else:
        # For any other error, print this and exit
        print('\033[31m[ERROR]\033[0m Cannot open this file'); sys.exit(1)



def search(password):
    check = requests.get('https://api.pwnedpasswords.com/pwnedpassword/%s' % password)

    breached = '%s seen [%s] times before' % (password, check.text)

    if check.status_code == 404:
        return ('\033[32m[SECURE]\033[0m'.ljust(40) + '%s') % password
    elif check.status_code == 200:
        return ('\033[31m[BREACHED]\033[0m'.ljust(40) + '%s' % breached)
    else:
        # Most likely an error, return secure
        return ('\033[32m[SECURE]\033[0m'.ljust(40) + '%s') % password

# Set sleep time
if args.burst == None:
    timer = '1.5'
else:
    timer = float(args.burst)


# Print a header
header = 'Status'.ljust(30), 'Password'
print('\033[94m{0[0]} {0[1]}\033[0m'.format(header))

if args.check == None:
    # Check passwords
    for l in passwords:
        if args.save == None:
            print(search(l.strip()))
            time.sleep(float(timer))

        else:
            result = search(l.strip())
            time.sleep(float(timer))

            with open(args.save, 'a+') as f:
                print(result)
                f.write(result.encode('utf-8') + '\n')
                f.close()
else:
    print(search(args.check))

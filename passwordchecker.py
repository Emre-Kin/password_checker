import requests
import hashlib
# Emre Kin 
# <yemrekin4@gmail.com>
#with this code you can look how many time your password hacked
def request_api_data(querry_char):
    url = 'https://api.pwnedpasswords.com/range/' + querry_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {res.status_code}, check the API and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':')for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    # check password if it exist in API response
    sha1password = hashlib.sha1(password.encode('utf_8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        response = pwned_api_check(password)
        if response:
            print(f'{password} was found {response} times.... you should change it')
        else:
            print(f'{password} was not found,You can use it')


if __name__ == '__main__':
    print('give the name of passwords file')
    sys.exit(main(input('your password :'))

import fileinput
import string

lines = [line.strip() for line in fileinput.input()]
passports = [{}]
for line in lines:
    if line == '':
        passports.append({})
    kvs = [kv.split(':') for kv in line.split()]
    passports[-1] |= {k:v for k,v in kvs}
valids = 0
for passport in passports:
    valid = len(passport) == 7 and 'cid' not in passport
    valid = valid or len(passport) == 8
    if not valid:
        continue
    valid = valid and passport['byr'].isnumeric()
    valid = valid and (1920 <= int(passport['byr']) <= 2002)
    valid = valid and passport['iyr'].isnumeric()
    valid = valid and (2010 <= int(passport['iyr']) <= 2020)
    valid = valid and passport['eyr'].isnumeric()
    valid = valid and (2020 <= int(passport['eyr']) <= 2030)
    hgt = passport['hgt']
    valid = valid and (hgt[-2:] in ('cm', 'in'))
    valid = valid and ((hgt[-2:] == 'cm' and 150 <= int(hgt[:-2]) <= 193) \
            or (hgt[-2:] == 'in' and 59 <= int(hgt[:-2]) <= 76))
    hcl = passport['hcl']
    valid = valid and hcl[0] == '#' and \
            all(c in string.hexdigits for c in hcl[1:]) and len(hcl[1:]) == 6
    valid = valid and (passport['ecl'] in 'amb blu brn gry grn hzl oth'.split())
    valid = valid and passport['pid'].isnumeric() and len(passport['pid']) == 9

    if valid:
        valids += 1
print(valids)

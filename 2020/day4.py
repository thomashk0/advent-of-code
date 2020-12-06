import itertools
import re


def collect_passports(f):
    passports = []
    fields = []
    for line in itertools.chain(f, ("\n",)):
        line = line.strip()
        if not line:
            passports.append(fields)
            fields = []
            continue
        for pair in line.split():
            k, v = tuple(pair.split(':'))
            fields.append((k, v))
    return passports


def validate_range(min, max, n_digits=0):
    def f(v):
        if n_digits and len(v) != n_digits:
            return False
        try:
            value = int(v)
            return min <= value <= max
        except ValueError:
            return False

    return f


class Validator:
    # key 'cid' is optional
    REQUIRED_KEYS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

    IYR_RE = re.compile(r"^(\d+)(cm|in)$")
    HCL_RE = re.compile(r"^#([0-9a-f]{6})$")
    ECL_VALUES = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

    @staticmethod
    def has_required_fields(p):
        p_keys = set(k for k, _ in p)
        if len(p_keys) != len(p):
            print("duplicated keys")
            return False
        missing_keys = Validator.REQUIRED_KEYS - p_keys
        # print("missing: ", missing_keys)
        return not missing_keys

    @staticmethod
    def validate(k, v) -> bool:
        f = getattr(Validator, f"validate_{k}", None)
        return f(v)

    @staticmethod
    def valid_passport(p) -> bool:
        return all(Validator.validate(k, v) for k, v in p)

    validate_byr = validate_range(1920, 2002, n_digits=4)
    validate_iyr = validate_range(2010, 2020, n_digits=4)
    validate_eyr = validate_range(2020, 2030, n_digits=4)

    @staticmethod
    def validate_hgt(v):
        r = Validator.IYR_RE.match(v)
        if not r:
            return False
        if r.group(1).startswith('0'):
            # Guessing: no trailing zero
            return False
        v = int(r.group(1))
        unit = r.group(2)
        if unit == 'cm':
            return 150 <= v <= 193
        elif unit == 'in':
            return 59 <= v <= 76
        else:
            return False

    @staticmethod
    def validate_hcl(v):
        r = Validator.HCL_RE.match(v)
        if not r:
            return False
        return True

    @staticmethod
    def validate_ecl(v):
        return v in Validator.ECL_VALUES

    validate_pid = validate_range(0, 999999999, n_digits=9)

    @staticmethod
    def validate_cid(_):
        return True


def test_validate():
    valid = [
        ('byr', '2002'),
        ('hgt', '60in'),
        ('hgt', '190cm'),
        ('hcl', '#123abc'),
        ('ecl', 'brn'),
        ('pid', '000000001'),
        ('cid', 'huhuhhuhu')
    ]
    for k, v in valid:
        assert Validator.validate(k, v)

    invalid = [
        ('byr', '1919'),
        ('byr', '01925'),
        ('byr', 'z1919'),
        ('byr', '2003'),
        ('hgt', '190in'),
        ('hgt', '190cmin'),
        ('hgt', '0190cm'),
        ('hgt', '190ci'),
        ('hgt', '190'),
        ('hcl', '#123abz'),
        ('hcl', '#123aa'),
        ('hcl', '123abz'),
        ('ecl', 'wat'),
        ('pid', '0123456789'),
        ('pid', '12345678')
    ]
    for k, v in invalid:
        assert not Validator.validate(k, v)


def test_invalid_example():
    passports = collect_passports(open('assets/day4-example-2'))
    assert len(passports) == 4
    valid_passports = list(filter(Validator.valid_passport, passports))
    assert len(valid_passports) == 0


def test_valid_example():
    passports = collect_passports(open('assets/day4-example-3'))
    assert len(passports) == 4
    valid_passports = list(filter(Validator.valid_passport, passports))
    assert len(valid_passports) == 4


def main():
    passports = collect_passports(open('assets/day4-input'))

    valid_passports = list(filter(Validator.has_required_fields, passports))
    print("part 1:", len(valid_passports))

    valid_passports = list(filter(Validator.valid_passport, valid_passports))
    print("part 2:", len(valid_passports))


if __name__ == '__main__':
    main()

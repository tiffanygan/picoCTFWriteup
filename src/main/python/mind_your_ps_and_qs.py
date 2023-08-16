import requests


def get_ps_and_qs(coprimes):
    ps_and_qs = []
    get_ps_and_qs_helper(ps_and_qs, coprimes, 0, 1, 1)
    return ps_and_qs


def get_ps_and_qs_helper(ps_and_qs, coprimes, idx, curr_factor_one, curr_factor_two):
    if idx == len(coprimes):
        ps_and_qs.append({curr_factor_one, curr_factor_two})
        return
    factor_one_new = curr_factor_one * pow(int(coprimes[idx][0]), int(coprimes[idx][1]))
    get_ps_and_qs_helper(ps_and_qs, coprimes, idx + 1, factor_one_new, curr_factor_two)
    factor_two_new = curr_factor_two * pow(int(coprimes[idx][0]), int(coprimes[idx][1]))
    get_ps_and_qs_helper(ps_and_qs, coprimes, idx + 1, curr_factor_one, factor_two_new)


if __name__ == '__main__':
    file_name = '../../resources/mind_your_ps_and_qs_values'

    with open(file_name, 'r') as f:
        for line in f:
            if line.startswith('c'):
                c = int(line.split(': ')[1])
            elif line.startswith('n'):
                n = int(line.split(': ')[1])
            elif line.startswith('e'):
                e = int(line.split(': ')[1])

    factor_db_url = 'http://factordb.com/api'
    params = {'query': n}
    r = requests.get(factor_db_url, params=params)

    if r.status_code == 200:
        response = r.json()
        coprime_factors = response['factors']
        ps_and_qs_pairs = get_ps_and_qs(coprime_factors)
        for pair in ps_and_qs_pairs:
            factor_one = list(pair)[0]
            factor_two = list(pair)[1]
            if factor_one == 1 or factor_two == 1:
                continue
            phi = (factor_one - 1) * (factor_two - 1)
            d = pow(e, -1, phi)
            m_num = pow(c, d, n)
            m_len = (m_num.bit_length() + 7) // 8
            m_bin = m_num.to_bytes(m_len, 'big')
            print(m_bin)

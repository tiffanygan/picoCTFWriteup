# file_name = '../../resources/mind_your_ps_and_qs_values'
#
# with open(file_name, 'r') as f:
#     line = f.readline()
#     num = line.split(' ')[1]
#     print(line.split(' ')[1])
#     print(num)
import base64

import requests

c = 8533139361076999596208540806559574687666062896040360148742851107661304651861689
# n = 18
n = 769457290801263793712740792519696786147248001937382943813345728685422050738403253
e = 65537

factor_db_url = 'http://factordb.com/api'
params = {'query': n}
r = requests.get(factor_db_url, params=params)

if r.status_code == 200:
    response = r.json()
    factors = response['factors']
    if len(factors) == 2:
        factor_one = pow(int(factors[0][0]), int(factors[0][1]))
        factor_two = pow(int(factors[1][0]), int(factors[1][1]))
        phi = (factor_one - 1) * (factor_two - 1)
        d = pow(e, -1, phi)
        m_num = pow(c, d, n)


        print(m)

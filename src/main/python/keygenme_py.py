import hashlib

username = b'MORTON'
username_hash = hashlib.sha256(username).hexdigest()
idx_order = [4, 5, 3, 6, 2, 7, 1, 8]
flag = 'picoCTF{1n_7h3_|<3y_of_'

for idx in idx_order:
    flag += username_hash[idx]

flag += '}'

print(flag)

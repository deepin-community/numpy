#!/usr/bin/python3

'''
Check if debian/versions is sane and generate substvars for numpy:Provides.
'''

import os
import pathlib

def main():
    setup_common = 'numpy/core/setup_common.py'
    data = {}
    with open(setup_common) as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith(('C_ABI_VERSION', 'C_API_VERSION')):
                key, _, value = line.split()
                data[key] = int(value, base=16)
    with open('debian/versions') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split(None, 1)
            data[key] = value
    assert data['abi'] == str(data['C_ABI_VERSION'] - 0x1000000), f"ABI version mismatch, update debian/versions; debian={data['abi']} vs numpy={str(data['C_ABI_VERSION'] - 0x1000000)}"
    assert data['api'] == str(data['C_API_VERSION']), f"API version mismatch, update debian/versions; debian={data['api']} vs numpy={str(data['C_API_VERSION'])}"
    print('numpy3:Provides=python3-numpy-abi%s, python3-numpy-api%s' % (data['abi'], data['api']))

if __name__ == '__main__':
    main()

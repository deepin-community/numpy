#!/usr/bin/python3

'''
Check if debian/versions is sane and generate substvars for numpy:Provides.
'''

import os
import re

def main():
    meson_build = 'numpy/_core/meson.build'
    data = {}
    with open(meson_build) as file:
        for line in file:
            line = line.strip()
            mo = re.match("(?i)^(C_ABI_VERSION|C_API_VERSION) *= *'(0x[0-9A-F]+)'", line)
            if mo:
                data[mo.group(1)] = int(mo.group(2), base=16)
                if "C_ABI_VERSION" in data and "C_API_VERSION" in data:
                    break
    with open('debian/versions') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split(None, 1)
            data[key] = value
    assert data['abi'] == str(data['C_ABI_VERSION'] - 0x2000000), f"ABI version mismatch, update debian/versions; debian={data['abi']} vs numpy={str(data['C_ABI_VERSION'] - 0x2000000)}"
    assert data['api'] == str(data['C_API_VERSION']), f"API version mismatch, update debian/versions; debian={data['api']} vs numpy={str(data['C_API_VERSION'])}"
    print('numpy3:Provides=python3-numpy2-abi%s, python3-numpy-api%s' % (data['abi'], data['api']))

if __name__ == '__main__':
    main()

#!/usr/bin/python3
# Architecture-specific long double formats for
# cross compilation
#
# This script expects two positional argument
# 1. the meson cross file
# 2. the DEB_HOST_ARCH architecture name
#
import configparser
import sys


class CaseSensitiveConfigParser(configparser.ConfigParser):
    optionxform = staticmethod(str)


cross_file = CaseSensitiveConfigParser()
with open(sys.argv[1]) as f:
    cross_file.read_file(f)

cross_file["properties"]["longdouble_format"] = repr(
    {
        "amd64": "INTEL_EXTENDED_16_BYTES_LE",
        "arm64": "IEEE_QUAD_LE",
        "armel": "IEEE_DOUBLE_LE",
        "armhf": "IEEE_DOUBLE_LE",
        "hppa": "IEEE_DOUBLE_BE",
        "i386": "INTEL_EXTENDED_12_BYTES_LE",
        "m68k": "MOTOROLA_EXTENDED_12_BYTES_BE",
        "mips64el": "IEEE_QUAD_LE",
        "ppc64": "IBM_DOUBLE_DOUBLE_BE",
        "ppc64el": "IBM_DOUBLE_DOUBLE_LE",
        "riscv64": "IEEE_QUAD_LE",
        "s390x": "IEEE_QUAD_BE",
        "sparc64": "IEEE_QUAD_BE",
    }.get(sys.argv[2], "UNKNOWN")
)

with open(sys.argv[1], "w") as f:
    cross_file.write(f)

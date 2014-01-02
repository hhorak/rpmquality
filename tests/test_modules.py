#!/usr/bin/python

import PackagesList, RpmLint
import os

test_packages_dir = "testpackages"
testingpackages = [ os.path.join(test_packages_dir, rpm) for rpm in os.listdir(test_packages_dir) ]
print("Testing packages:")
for rpm in testingpackages:
    print(rpm)

p=RpmLint.RpmLint(scl_name="mysql55", packages=testingpackages)
print("Result of RpmLint is:")
print(p.perform())

p=PackagesList.PackagesList(scl_name="mysql55", packages=testingpackages)
print("Result of PackagesList is:")
print(p.perform())



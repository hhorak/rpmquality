#!/usr/bin/python

import RpmQuality
import os

test_packages_dir = "modules/testpackages"
testingpackages = [ os.path.join(test_packages_dir, rpm) for rpm in os.listdir(test_packages_dir) ]
print("Testing packages:")
for rpm in testingpackages:
    print(rpm)


s = RpmQuality.RpmQuality(packages=testingpackages, scl_name="mysql55")
s.performAll()




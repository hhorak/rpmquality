import re
import os
import DefaultModule

class PackagesList(DefaultModule.DefaultModule):

    _log_file = "packagelist.log"

    def perform(self):
        self._touch_log()
        if not self._scl_name:
            return False

        self._score = 100
        for package in self._packages:
            package_basename = os.path.basename(package)
            if not re.match("^%s" % self._scl_name, package_basename):
                self._log_warning("Package %s has suspicious name that doesn't begin with scl name %s." % (package_basename, self._scl_name))
                self._score /= 2

        if self._score < 0:
            self._score = 0
        return {"score": self._score}


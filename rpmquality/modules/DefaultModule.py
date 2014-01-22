import os

class DefaultModule:
    def __init__(self, scl_name=None, packages=[], log_file=None, working_dir=None):
        if log_file:
            self._log_file = log_file
        self._packages = packages
        self._scl_name = scl_name
        self._score = 0
        self._packages_attr = {}
        self._working_dir = working_dir

    def _log_warning(self, message):
        with open(self._log_file, "a") as f:
            f.write("%s\n" % message)

    def _touch_log(self):
         with open(self._log_file, "a") as f:
             os.utime(self._log_file, None)

    def _get_working_dir(self):
        if not os.path.exists(self._working_dir):
            os.mkdir(self._working_dir, 0644)
        return self._working_dir

    def _is_src():
        if not package in self._packages_attr or not "src" in self._packages_attr[package]:
            self._packages_attr[package]["src"] = bool(re.match(r".*\.src\.rpm$", package))
        return self._packages_attr[package]["src"]


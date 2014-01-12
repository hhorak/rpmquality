class DefaultModule:
    def __init__(self, scl_name=None, packages=[], log_file=None):
        if log_file:
            self._log_file = log_file
        self._packages = packages
        self._scl_name = scl_name
        self._score = 0

    def _log_warning(self, message):
        with open(self._log_file, "a") as f:
            f.write("%s\n" % message)


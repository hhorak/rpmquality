import re
import subprocess
import DefaultModule
import locale

class RpmLint(DefaultModule.DefaultModule):
    """
    Uses rpmlint utility and parses its output.
    """

    _errors_to_ignore = [ ]
    _errors_to_ignore_scl = [ "dir-or-file-in-opt" ]
    _errors_multiplyer = { "E": 75, "W": 95 }
    _log_file="rpmlint.log"

    def _check_rpmlint_output(self, output):
       error_types_present = { "E": {}, "W": {} }
       
       # last line is resutl summary, ignore it
       for line in output.split("\n")[0:-1]:
           # some messages contain line number
           match = re.match(r"^(?P<pkgname>[^:]+):(\d+:)?\s+(?P<errtype>[WE]):"
                             "\s+(?P<errname>\S+)", line)
           if match:
               error_type = match.group("errtype")
               error_message = match.group("errname")
               if self._scl_name and  error_message in self._errors_to_ignore:
                   continue
               if error_message in self._errors_to_ignore:
                   continue
               if not error_message in error_types_present[error_type]:
                   error_types_present[error_type][error_message] = 1
               else:
                   error_types_present[error_type][error_message] += 1
               self._log_warning(line)

       score = 100
       for err in ["E", "W"]:
           for i in range(len(error_types_present[err].keys())):
               score = score * self._errors_multiplyer[err] / 100

       return score
           

    def perform(self):
        self._touch_log()
        for package in self._packages:
            sub_score = 0
            files_checked = 0
            try:
                print("Calling %s %s" % ("rpmlint", package))
                encoding = locale.getdefaultlocale()[1]
                out = subprocess.check_output(["rpmlint", package]).decode(encoding)

            except subprocess.CalledProcessError as e:
                out = e.output
                
            files_checked += 1
            sub_score += self._check_rpmlint_output(out)

        if files_checked > 0:
            self._score = sub_score / files_checked
        else:
            self._score = 0

        return {"score": self._score}


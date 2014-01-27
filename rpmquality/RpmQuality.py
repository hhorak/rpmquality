import os
import sys

class RpmQuality:
    """
    Wrapper and collector for particular quality modules
    """

    # key is module name, value is importance (weight)
    _modules = {}
    _basic_modules = {"PackagesList": 10,
                      "RpmLint": 30}

    def __init__(self, packages=[], scl_name=None, logs_location="logs",
                 extra_modules_dir=None, extra_modules={}, working_dir=None):
        self._app_root = os.path.dirname(os.path.abspath(__file__))
        self._packages = packages
        self._scl_name = scl_name
        self._modules_dir = os.path.join(self._app_root, "modules")
        self._extra_modules_dir = extra_modules_dir
        self._extra_modules = extra_modules
        self._weights_sum = self._weights_sum_compute()
        self._logs_location = logs_location
        self._working_dir = working_dir

    def _weights_sum_compute(self):
        """
        Loops through all modules and computes sum of their weight
        """
        sum = 0
        for weight in self._modules.values():
            sum += weight
        return sum
            

    def performAll(self):
        """
        Calls particular quality modules.
        Returns dict in format
        {
            score: 0-100,
            results:
                [
                    {
                        module: module1name,
                        score: 0-100,
                        logfile: results.log
                    },
                    {
                        module: module2name,
                        score: 0-100,
                        logfile: results2.log
                    }
                ]
        }
        """
        
        # add modules and extra_modules paths to search path
        modules_path = os.path.abspath(self._modules_dir) 
        if not modules_path in sys.path:
            print(modules_path)
            sys.path.insert(1, modules_path)
       
        if self._extra_modules_dir:
            extra_modules_path = os.path.abspath(self._extra_modules_dir) 
            if not extra_modules_path in sys.path:
                print(extra_modules_path)
                sys.path.insert(1, extra_modules_path)

        final_score = 0
        final_results = {"score": 0, "results": []}

        # create logs and working directories if not exist
        if not os.path.isdir(self._logs_location):
            os.makedirs(self._logs_location, 0o755)
        if not os.path.isdir(self._working_dir):
            os.makedirs(self._working_dir, 0o755)

        self._modules = self._basic_modules.copy()
        self._modules.update(self._extra_modules.items())
        for module_name in self._modules:
            # where we want results (log), working directory, etc.
            log_file = os.path.join(self._logs_location, "%s.log" % module_name)
            # working_dir = os.path.join(self._working_dir, logs_location, "%s-working" % module_name)

            # import every module separately
            mod_obj = __import__(module_name, fromlist = [])
            mod_class = getattr(mod_obj, module_name)
            old_cwd = os.path.abspath(os.path.curdir)
            os.chdir(self._working_dir)
            mod_inst = mod_class(scl_name = self._scl_name,
                                 packages = self._packages,
                                 log_file = log_file,
                                 working_dir = self._working_dir)
            os.chdir(old_cwd)
            
            # perform the test
            result = mod_inst.perform()

            # do something with results
            result_score = result["score"]
            if "weight" in result:
                self._modules[module_name] = result["weight"]

            # store results and their weighted score
            final_score += result_score * self._modules[module_name]
            final_results["results"].append({"module": module_name,
                                             "score": result_score,
                                             "logfile": log_file})

        # compute
        final_results["score"] = final_score / self._weights_sum_compute()
    
        return final_results


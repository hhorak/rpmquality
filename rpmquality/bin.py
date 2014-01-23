#!/usr/bin/python

import RpmQuality

import sys
import os
import re
import datetime


def version():
    progname = os.path.basename(__file__)
    print("%s 0.1" % progname)
    print
    print("Written by Honza Horak <hhorak@redhat.com>")
    exit(0)

def usage():
    progname = os.path.basename(__file__)
    print("%s analysis quality of individual RPM packages and reports various kinds of results" % progname)
    print
    print("Usage: %s package [ package, package, dir, ... ]" % progname)
    print
    print("Options:")
    print("  -h, --help             Prints help")
    print("  -V, --version          Prints version info")
    print("  -v, --verbose          Prints more verbose degug output during scan")
    print("  -l, --logdir           Change log file location of result, default: /var/tmp/rpmqualityYYYYmmddHHMMSS/logs")
    print("  -w, --working-dir      Change log file location of result, default: /var/tmp/rpmqualityYYYYmmddHHMMSS/working_dir")
    print("  -s, --sclname          Name of the Software Collection if aplicable for the package")
    print
    print("Examples:")
    print("  %s -h" % progname)
    print("  %s -v foo.rpm bar.rpm" % progname)
    print("  %s -l /var/tmp/foo foo.rpm" % progname)
    print("  %s -w /var/tmp/bar foo.rpm" % progname)
    print("  %s --sclname foo42 foo42-foo.rpm" % progname)
    exit(1)


def print_result(result):
    """
    Prints results well formated.
    """
    print("Total score: %s" % result["score"])
    for module_data in result["results"]:
        print("Module %s score: %s" % (module_data["module"], module_data["score"]))
        print("Module %s logfile: %s" % (module_data["module"], module_data["logfile"]))


def main():
    verbose = False
    packages = []
    scl_name = None
    tmp_dir = "/var/tmp/rpmquality%s" % datetime.datetime.now().strftime('%Y%m%d%H%M%S%Z')
    logs = os.path.join(tmp_dir, "logs")
    working_dir = os.path.join(tmp_dir, "working_dir")

    # parsing arguments
    args = list(sys.argv)
    args.reverse()
    args.pop()
    while args:
        arg = args.pop()
        if arg == "-h" or arg == "--help":
            usage()
        if arg == "-V" or arg == "--version":
            version()
        elif arg == "-v" or arg == "--verbose":
            verbose = True
        elif args and (arg == "-l" or arg == "--logs"):
            logs = args.pop()
        elif args and (arg == "-w" or arg == "--working-dir"):
            working_dir = args.pop()
        elif args and (arg == "-s" or arg == "--scl"):
            scl_name = args.pop()
        else:
            if os.path.isfile(arg) and re.match(r".*\.rpm$", arg):
                packages.append(os.path.abspath(arg))
            elif os.path.isdir(arg):
                for f in os.listdir(arg):
                    if re.match(r".*\.rpm$", f):
                        packages.append(os.path.abspath(os.path.join(arg, f)))
            else:
                print("Argument %s is not rpm nor valid argument." % arg)
                usage()

    if not packages:
        print("No packages specified.")
        usage()

    if not scl_name:
        regexp = re.compile(r"^(\w+)-build.*")
        for pkg in packages:
            m = regexp.match(os.path.basename(pkg))
            if m:
                scl_name = m.group(1)
                break
        regexp = re.compile(r"^(\w+)-.*")
        pkg = os.path.basename(packages[0])
        m = regexp.match(pkg)
        if m:
            scl_name = m.group(1)

    if verbose:
        print("Verbose: %s" % verbose)
        print("SCL name: %s" % scl_name)
        print("Logs location: %s" % logs)
        print("Working directory location: %s" % working_dir)
        print("Packages:")
        for rpm in packages:
            print(rpm)

    rp = RpmQuality.RpmQuality(packages=packages, scl_name=scl_name,
                               logs_location=logs, working_dir=working_dir
                               #,
                               #extra_modules_dir="softwarecollectios_modules",
                               #extra_modules={"UserFavour": 60},
                               #user_id="pepa"
                               )
    result = rp.performAll()
    print_result(result)


if __name__ == "__main__":
    main()




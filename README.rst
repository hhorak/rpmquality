rpmquality
=====
rpmquality analysis quality of individual RPM packages and reports various kinds of results

rpmquality is licensed under MIT License

Usage: rpmquality package [ package, package, dir, ... ]

Options:
  -h, --help             Prints help
  -V, --version          Prints version info
  -v, --verbose          Prints more verbose degug output during scan
  -l, --logdir           Change log file location of result, default: /var/tmp/rpmqualityYYYYmmddHHMMSS/logs
  -w, --working-dir      Change log file location of result, default: /var/tmp/rpmqualityYYYYmmddHHMMSS/working_dir
  -s, --sclname          Name of the Software Collection if aplicable for the package

Examples:
  rpmquality -h
  rpmquality -v foo.rpm bar.rpm
  rpmquality -l /var/tmp/foo foo.rpm
  rpmquality -w /var/tmp/bar foo.rpm
  rpmquality --sclname foo42 foo42-foo.rpm


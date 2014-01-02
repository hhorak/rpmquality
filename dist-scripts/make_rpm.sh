#!/bin/sh

if [ $# -ne 1 ] ; then
    echo "Usage: `basename $0` --source|--binary"
    exit 1
fi

RPMBUILD_DIR=~/rpmbuild
latest_tar=`ls -t rpmquality*tar.gz | head -n 1`
if [ -z "$latest_tar" ] ; then
    echo "No tar ball found."
    exit 1
fi

mkdir -p "${RPMBUILD_DIR}/SOURCES/" "${RPMBUILD_DIR}/SPECS/"
cp -f $latest_tar "${RPMBUILD_DIR}/SOURCES/"
cp -f dist/rpmquality.spec "${RPMBUILD_DIR}/SPECS/"

if [ $1 == "--source" ] ; then
    echo "rpmbuild -bs ${RPMBUILD_DIR}/SPECS/rpmquality.spec"
    rpmbuild -bs "${RPMBUILD_DIR}/SPECS/rpmquality.spec"
elif [ $1 == "--binary" ] ; then
    echo "rpmbuild -bb ${RPMBUILD_DIR}/SPECS/rpmquality.spec"
    rpmbuild -bb "${RPMBUILD_DIR}/SPECS/rpmquality.spec"
fi

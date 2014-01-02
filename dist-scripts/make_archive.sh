#!/bin/sh

if [ $# -ne 1 ] ; then
    echo "Usage: `basename $0` version"
    exit 1
fi

ARCHIVE_DIR="rpmquality-$1"
rm -rf $ARCHIVE_DIR
mkdir $ARCHIVE_DIR

cp -p --parents ./dist/*.spec $ARCHIVE_DIR
cp -p --parents ./src/softwarecollectios_modules/*.py $ARCHIVE_DIR
cp -p --parents ./src/modules/*.py $ARCHIVE_DIR
cp -p --parents ./src/*.py $ARCHIVE_DIR
cp -p ./README ./LICENSE $ARCHIVE_DIR

tar -pczvf "${ARCHIVE_DIR}.tar.gz" $ARCHIVE_DIR

rm -rf $ARCHIVE_DIR


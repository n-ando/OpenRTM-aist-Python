#!/bin/sh

echo "<<< ComponentObserverConsumer Test setup start >>>"

# idl file copy
cp -pf ../../../RTM_IDL/RTC.idl .
cp -pf ../../../RTM_IDL/SDOPackage.idl .

# idl file compile
omniidl -bpython *.idl

echo "<<< ComponentObserverConsumer Test setup Complete >>>"
echo ""


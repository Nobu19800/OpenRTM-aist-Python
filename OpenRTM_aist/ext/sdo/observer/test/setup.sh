#!/bin/sh

echo "<<< ComponentObserverConsumer Test setup start >>>"

# idl file copy
cp -pf ../../../../RTM_IDL/BasicDataType.idl .
cp -pf ../../../../RTM_IDL/DataPort.idl .
cp -pf ../../../../RTM_IDL/OpenRTM.idl .
cp -pf ../../../../RTM_IDL/RTC.idl .
cp -pf ../../../../RTM_IDL/SDOPackage.idl .
cp -pf ../ComponentObserver.idl .
cp -pf ../../../RTM_IDL/SharedMemory.idl .
cp -pf ../../../RTM_IDL/IORProfile.idl .

# idl file compile
omniidl -bpython *.idl

echo "<<< ComponentObserverConsumer Test setup Complete >>>"
echo ""


@echo off
echo "<<< ComponentObserverConsumer setup start >>>"

set idlfiles=RTC.idl SDOPackage.idl

rem # idl file copy
for %%x in (%idlfiles%) do copy ..\..\..\RTM_IDL\%%x .

rem # idl file compile
set idlfiles=%idlfiles% ComponentObserver.idl
for %%x in (%idlfiles%) do omniidl -I. -bpython %%x

echo "<<< ComponentObserverConsumer setup Complete >>>"
echo ""


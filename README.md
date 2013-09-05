saphub
======

A command-line tool to deploy an Hana XS Engine project from a local folder to a Hana instance. The contents of the local folder will overwrite the entire contents of the Hana package it it exists already.

saphub.py
---------

Download saphub.py to your dev machine and execute run in the folder you that contains the Hana package you want to deploy

    /folder/to/project> python saphub.py --host <hana ip:port> --usr <hana user> --pwd <hana password> --package <hana package name> --saphub <saphubd ip:port>

saphubd.py
----------

Download saphubd.py to the Hana server or any other server that has regi installed and run, now called the saphubd server

    > python saphubd.py --port=<port> --regi=</full/path/to/regi>

Dependencies
------------

 - saphub.py
   - python 2.7 or higher

 - saphubd.py
   - python 2.7 or higher
   - regi

Hint
----

Make sure that
- you dev machine can ping the saphubd server
- the saphubd server can ping the Hana server

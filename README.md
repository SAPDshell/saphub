saphub
======

A command-line tool to deploy an Hana XS Engine project from a local folder to a Hana instance.

saphub.py
---------

    /folder/to/project> python saphub.py --host <hana ip:port> --usr <hana user> --pwd <hana password> --package <hana package name> --saphub <saphubd ip:port>

saphubd.py
----------

    > python saphubd.py --port=<port> --regi=</full/path/to/regi>

Dependencies
------------

 - saphub.py
   - python 2.7 or higher

 - saphubd.py
   - python 2.7 or higher
   - regi

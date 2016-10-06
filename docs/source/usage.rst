#####
Usage
#####


*****
Build
*****

Executes the project build in a given path.

Args:
  :param --path: the project root folder

Example:

  .. code-block:: bash

     abcd build --path /app


*******
Inspect
*******

Inspect the project file structure.

Args:
  :param --path: the project root folder

Example:

  .. code-block:: bash

     abcd inspect --path /app



******
Export
******

Gets the build output file path (APK files for anroid).

Args:
  :param --path: the project root folder

Example:

  .. code-block:: bash

     abcd export --path /app


******
Log
******

Reads the content of the build log files.

Args:
  :param --path: the project root folder
  :param --ctx: the log context (build, validate or all)

Example:

  .. code-block:: bash

     abcd log --path /app

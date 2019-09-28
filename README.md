## getdiskusage.py

### Purpose
Prints list of all the files on the mountpoint and their disk usage in bytes in json format.

### Example

$ getdiskusage.py /tmp

{
    "files": {
        "/tmp/foo": 1000,
        "/tmp/bar": 1000000,
        "/tmp/buzzz": 42
    }
}

### Requirements
Requires at least Python 2.6 because of json library.

### Tests carried out to check the functionality.

All these are executed in the command prompt by traversing to the directory where the python file (getdiskusage.py) is saved.

python getdiskusage.py /foobar

output -- /foobar The entered directory does not exists


python getdiskusage.py foobar

output -- foobar This is not a directory


python getdiskusage.py /root

output -- /root You are not authorized to access this folder



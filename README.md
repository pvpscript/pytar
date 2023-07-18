# pytar
An extremely simple tar wrapper that adds data as files in a tarball

# Introduction
I wrote this code for a script I was writing that required raw data to be added as files and compressed inside a tarball. It makes use of the native python lib, [tarfile](https://docs.python.org/3/library/tarfile.html)

# Usage
```python
with Tar('/home/user/filename.tar.gz') as tarball:
    tarball.add_file('hello.txt', 'Hello, World!')
    tarball.add_file('bye.txt', 'Goodbye, World!')
```

The example above will create, in the `/home/user` path, a file called `filename.tar.gz` that will have two files, `hello.txt` and `bye.txt`.

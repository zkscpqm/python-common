# Python STL extensions

---

authors: zkscpqm

developer contact: zkscpqm@daum.net

---

## What is this repo?

If you've ever been put on a new Python project and been forced to write the same boilerplate code over and over again,
this library is for you. There's nothing groundbreaking or "new" here, just the things you'd rather not waste your time
writing. Things like lazy properties, threads with return values or callbacks, a wrapper for boto3's un-pythonic API etc.


## How do I use these resources?

There's a high chance you won't use everything here. Copy the files to your project, fix the imports (make sure to check 
whether a file you want imports anything else from the repo. At the very least it will require `types_extensions`.


## Requirements

Most of the resources have no 3rd-party requirements. Obviously any AWS wrapper will need `boto3`, any web request macros
will need `requests` or `urllib3` etc. For now a minimum python version required is `3.10rc01`. Compatibility with older
versions will be done eventually.


## Contributing

If you're seeing this section here it's because I've been too lazy to make a `CONTRIBUTING` file.

Rules:

1. Everything **MUST** be typed, including `None` returns. There are extra type extensions and macros in the file `types_extensions.py` (no shit)
2. Don't create dependencies for outdated libraries that haven't been touched since the stone ages. If such a library is required, chances are whatever you're writing doesn't belong here.
3. If you write any `.c` or `.cu` extensions, make sure you have a `.pyi` file and a `README.md` in the parent directory of your code with compilation instructions (including compiler versions)
4. Spaghetti belongs in a bowl or on a sweater, not in this repo. Make sure you write clean code.

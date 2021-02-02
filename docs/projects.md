---
layout: default
title: Projects
tagline: An invitation to aerospace control
description: This is the course website for Aerospace Control Systems
---

## Contents
{:.no_toc}

* This text will be replaced by a table of contents (excluding the above header) as an unordered list
{:toc}

---

## Installation

### Python

We recommend the use of [conda](https://docs.conda.io/) to install python by following the instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/). We strongly recommend that you use the **Miniconda installer** instead of the Anaconda installer.

To confirm that installation was successful, do three things.

First, open a terminal and run `conda list`. You should see something like this:
```
(base) timothybretl@Timothys-MacBook-Pro Website % conda list
# packages in environment at /Users/timothybretl/Applications/miniconda3:
#
# Name                    Version                   Build  Channel
brotlipy                  0.7.0           py38h9ed2024_1003  
ca-certificates           2021.1.19            hecd8cb5_0  
certifi                   2020.12.5        py38hecd8cb5_0  
cffi                      1.14.4           py38h2125817_0  
chardet                   4.0.0           py38hecd8cb5_1003  
conda                     4.9.2            py38hecd8cb5_0  
conda-package-handling    1.7.2            py38h22f3db7_0  
cryptography              3.3.1            py38hbcfaee0_0  
idna                      2.10               pyhd3eb1b0_0  
libcxx                    10.0.0                        1  
libedit                   3.1.20191231         h1de35cc_1  
libffi                    3.3                  hb1e8313_2  
ncurses                   6.2                  h0a44026_1  
openssl                   1.1.1i               h9ed2024_0  
pycosat                   0.6.3            py38h1de35cc_1  
pycparser                 2.20                       py_2  
pyopenssl                 20.0.1             pyhd3eb1b0_1  
pysocks                   1.7.1                    py38_1  
python                    3.8.3                h26836e1_1  
python.app                2                       py38_10  
readline                  8.0                  h1de35cc_0  
requests                  2.25.1             pyhd3eb1b0_0  
ruamel_yaml               0.15.87          py38haf1e3a3_1  
setuptools                51.3.3           py38hecd8cb5_4  
six                       1.15.0           py38hecd8cb5_0  
sqlite                    3.33.0               hffcf06c_0  
tk                        8.6.10               hb0a8c7a_0  
tqdm                      4.55.1             pyhd3eb1b0_0  
urllib3                   1.26.2             pyhd3eb1b0_0  
xz                        5.2.5                h1de35cc_0  
yaml                      0.2.5                haf1e3a3_0  
zlib                      1.2.11               h1de35cc_3  
```

Second, in the same terminal, run `which python`. You should see something like this (crucially, with *miniconda3* in the path somewhere):
```
(base) timothybretl@Timothys-MacBook-Pro Website % which python
/Users/timothybretl/Applications/miniconda3/bin/python
```

Third, in the same terminmal, run `python` (and compute the sum `1 + 2`). You should see something like this:
```
(base) timothybretl@Timothys-MacBook-Pro Website % python
Python 3.8.3 (default, May 19 2020, 13:54:14)
[Clang 10.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 1 + 2
3
>>>
```

### Pybullet

One reason to use conda is that it is then easy to install everything else. Do the following two things to setup an environment in which you can run examples with pybullet.

First, create a text file named `ae353-bullet.yml` with the following contents (a file exactly like this can be downloaded from [here](https://github.com/tbretl/ae353-sp21/blob/main/examples/ae353-bullet.yml)):
```
name: ae353-bullet
channels:
  - defaults
dependencies:
  - numpy
  - scipy
  - matplotlib
  - pip
  - python=3
  - pip:
    - pybullet
    - notebook
```

Second, open a terminal, navigate to the folder containing `ae353-bullet.yml`, and run this command:
```
conda env create -f ae353-bullet.yml
```

To confirm that installation was successful, in the same terminal, do two things.

First, activate your new environment with `conda activate ae353-bullet`:
```
(base) timothybretl@Timothys-MacBook-Pro Website % conda activate ae353-bullet
(ae353-bullet) timothybretl@Timothys-MacBook-Pro Website %
```

Second, start python and `import pybullet`:
```
(ae353-bullet) timothybretl@Timothys-MacBook-Pro Website % python
Python 3.9.1 (default, Dec 11 2020, 06:28:49)
[Clang 10.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pybullet
pybullet build time: Jan 22 2021 10:46:31
>>>
```

### Jupyter notebooks

Notebooks are a convenient way to play around, to debug code, and to share results. To use notebooks with your new environment (`ae353-bullet`), you need to install an ipython kernel that corresponds to this environment (see [here](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)). In a terminal, do this:
```
python -m ipykernel install --user --name ae353-bullet --display-name "Python (ae353-bullet)"
```

Now you can open a notebook. In the same terminal, do this:
```
jupyter notebook
```

You should see something like this:
```
(ae353-bullet) timothybretl@Timothys-MacBook-Pro Website % jupyter notebook
[I 09:59:21.692 NotebookApp] Serving notebooks from local directory: /Users/timothybretl/Documents/courses/AE353/09 - AE353 (Spring 2021)/Website
[I 09:59:21.692 NotebookApp] Jupyter Notebook 6.2.0 is running at:
[I 09:59:21.692 NotebookApp] http://localhost:8888/?token=ff495f67918f4a8a4efd5e8cc1980cb1821ba2a58632b822
[I 09:59:21.692 NotebookApp]  or http://127.0.0.1:8888/?token=ff495f67918f4a8a4efd5e8cc1980cb1821ba2a58632b822
[I 09:59:21.692 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 09:59:21.708 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///Users/timothybretl/Library/Jupyter/runtime/nbserver-1848-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/?token=ff495f67918f4a8a4efd5e8cc1980cb1821ba2a58632b822
     or http://127.0.0.1:8888/?token=ff495f67918f4a8a4efd5e8cc1980cb1821ba2a58632b822
```

And, most importantly, your browser should open a page with a jupyter notebook.

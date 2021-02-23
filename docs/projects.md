---
layout: default
title: Projects
tagline: An invitation to aerospace control
description: How to get started on your design projects
---

## Contents
{:.no_toc}

* This text will be replaced by a table of contents (excluding the above header) as an unordered list
{:toc}

---

# Design Project \#1

### The system

The first project that you will complete this semester is to design, implement, and test a controller that uses a single-gimbal control moment gyroscope (CMG) to reorient a platform, as pictured below:

![Image of control moment gyroscope](./images/cmg.png)

This system has three parts:

* A *platform* (dark blue) that can rotate freely about its base. Think of this as a spacecraft that is confined to rotate about a single axis, as if it were being tested on the ground.
* A *gimbal* (light blue) that can be driven by a motor to rotate about a perpendicular axis with respect to the platform.
* A *rotor* (orange) that can be driven by a motor to spin about yet another perpendicular axis with respect to the gimbal.

If the rotor is spun at a high rate, then an "input torque" applied to the gimbal will, through conservation of angular momentum, result in an "output torque" applied to the platform. This output torque can be used, in particular, to change the orientation of the platform.

One advantage of using a single-gimbal CMG over a reaction wheel is that this output torque can be much higher than the input torque --- a so-called "torque amplification" effect. One disadvantage of using a CMG is that the resulting dynamics are more complicated and require a more sophisticated controller.

You can read more about CMGs and their use for spacecraft attitude control in [Fundamentals of Spacecraft Attitude Determination and Control (Markley and Crassidis, 2014)](https://link.springer.com/book/10.1007/978-1-4939-0802-8).

The motion of the system is governed by the following ordinary differential equations:

$$
\begin{aligned}
\dot{v}_1 &= - \left( \dfrac{5 \left(200 \tau_{3} \sin{\left(q_{2} \right)} + \sin{\left(2 q_{2} \right)} v_{1} v_{2} + 2 \cos{\left(q_{2} \right)} v_{2} v_{3}\right)}{10 \sin^{2}{\left(q_{2} \right)} - 511} \right) \\[1em]
\dot{v}_2 &= \dfrac{10 \left(100 \tau_{2} - \cos{\left(q_{2} \right)} v_{1} v_{3}\right)}{11} \\[1em]
\dot{v}_3 &= - \left( \dfrac{51100 \tau_{3} + 5 \sin{\left(2 q_{2} \right)} v_{2} v_{3} + 511 \cos{\left(q_{2} \right)} v_{1} v_{2}}{10 \sin^{2}{\left(q_{2} \right)} - 511} \right) \end{aligned}
$$

In these equations:

* $q_1$ and $v_1$ are the angle (rad) and angular velocity (rad/s) of the platform
* $q_2$ and $v_2$ are the angle (rad) and angular velocity (rad/s) of the gimbal
* $v_3$ is the angular velocity (rad/s) of the rotor
* $\tau_2$ is the torque (N$\cdot$m) applied by the platform to the gimbal
* $\tau_3$ is the torque (N$\cdot$m) applied by the gimbal to the rotor

Sensors provide measurements of all angles and angular velocities. Actuators allow you to choose what torques will be applied, up to a maximum of $\pm 5\;\text{N}\cdot\text{m}$.

The code provided [here]({{ site.github.repository_url }}/tree/main/projects/01_cmg) simulates the motion of this system ([CMGDemo]({{ site.github.repository_url }}/tree/main/projects/01_cmg/CMGDemo.ipynb)) and also derives the equations of motion in symbolic form ([DeriveEOM]({{ site.github.repository_url }}/tree/main/projects/01_cmg/DeriveEOM.ipynb)).

The system starts with the rotor spinning at 100 revolutions per minute and with zero platform and gimbal angles. The goal is to reorient the platform so it comes back to rest at a particular angle that you get to choose.

### Your tasks

First, do all of these things:

* Choose a platform angle that you want to achieve.
* Linearize the model about your chosen platform angle and express the result in state-space form.
* Design a linear state feedback controller and verify that the closed-loop system is asymptotically stable in theory.
* Implement this controller and plot the results as evidence to verify that the closed-loop system is asymptotically stable in simulation.

Then, consider at least one of the following questions:

* Is there a difference between the trajectory that is predicted by your linear model and the one that results from the nonlinear simulation?
* How do the initial conditions affect the resulting motion?
* How does the choice of goal angle affect the resulting motion?
* Does your controller still work if you change the rotor speed?

You are also welcome to consider a similar question that you come up with on your own.

### Your deliverables (by Monday, March 1)

#### Video

This video will satisfy the following requirements:

* It must show your working control system.
* It must visualize your answer to one question that you considered.
* It must include some description (e.g., as text or voice) of what is being shown.
* It must stay professional (use good sense, please).

It is best if this video is created by direct screen-capture rather than, for example, by taking a video of the screen with a cell phone.

It is best if this video is about 60 seconds in length --- it will be hard to show off your work with anything shorter, and it will be hard to keep viewers' attention with anything longer.

Submit your video by uploading it to the [AE353 (Spring 2021) Project Videos](https://mediaspace.illinois.edu/channel/channelid/201808523) channel on Illinois Media Space. Please take care to do the following:

* Use a descriptive title that includes your name in parentheses --- for example, "CMG control of a spacecraft (Tim Bretl)".
* Add the tag `P1` (an **upper case** "P" followed by the number "1"), so viewers can filter by project number.

You are welcome to resubmit your video at any time. To do so, please "Edit" your **existing** video and then do "Replace Media". Please do **not** create a whole new submission.

#### Code

This code will satisfy the following requirements:

* It must be in a folder called `01_code` (all numbers and **lower case**).
* It must include a single notebook called `GenerateResults.ipynb` that could be used by any of your peers to reproduce *all* of the results that you show in your video and your report.
* It must include all the other files (with the right directory structure) that are necessary for `GenerateResults.ipynb` to function.
* It must not rely on any dependencies other than those associated with the conda environment described by `ae353-bullet.yml`.

Submit your code by uploading it to Box in the [AE353 (Spring 2021) Project Submissions](https://uofi.box.com/s/56ieq301xo6dp334j2hbsr2ypvqebjku) folder.

In particular, you will find a sub-folder there with your NetID as the title. For instance, I would look for a sub-folder with the title `tbretl`. You have been made an "Editor" of your own sub-folder and so can upload, download, edit, and delete files inside this sub-folder. **Please keep your sub-folder clean and organized!** After submission of your first design project, your sub-folder should look like this:

```
yournetid
│   01_report.pdf
└───01_code
│   │   GenerateResults.ipynb
│   │   ae353-cmg.py
│   └───urdf
│       │   checker_blue.png
│       │   cmg.urdf
│       │   cmg_inner.stl
│       │   cmg_outer.stl
│       │   cmg_wheel.stl
│       │   plane.mtl
│       │   plane.obj
│       │   plane.urdf
|       ...
```

You are welcome to resubmit your code at any time. To do so, please **replace** your existing code. Please do not create new folders or move old ones to `01_code_old` or anything like that.

#### Report

This report will satisfy the following requirements:

* It must be a single PDF document that is called `01_report.pdf` and that conforms to the guidelines for [Preparation of Papers for AIAA Technical Conferences](https://www.aiaa.org/events-learning/events/Technical-Presenter-Resources). In particular, you must use either the [Word](https://www.aiaa.org/docs/default-source/uploadedfiles/aiaa-forums-shared-universal-content/preparation-of-papers-for-technical-conferences.docx?sfvrsn=e9a97512_10) or [LaTeX](https://www.overleaf.com/latex/templates/latex-template-for-the-preparation-of-papers-for-aiaa-technical-conferences/rsssbwthkptn#.WbgUXMiGNPZ) manuscript template.
* It must have a descriptive title, an author, an abstract, and a list of nomenclature.
* It must say how you addressed all of the required tasks (see above).
* It must **tell a story** that shows you have found and explored something that interests you.
* It must **acknowledge and cite** any sources, including the reports of your colleagues.

You may organize your report however you like, but a natural structure might be to have sections titled Introduction, Model, Design, Results, and Conclusion.

It is best if this report is about 5 pages in length --- it will be hard to show off your work with anything shorter, and it will be hard to keep readers' attention with anything longer.

Submit your report by uploading it to Box in the [AE353 (Spring 2021) Project Submissions](https://uofi.box.com/s/56ieq301xo6dp334j2hbsr2ypvqebjku) folder.

In particular, you will find a sub-folder there with your NetID as the title. For instance, I would look for a sub-folder with the title `tbretl`. You have been made an "Editor" of your own sub-folder and so can upload, download, edit, and delete files inside this sub-folder. **Please keep your sub-folder clean and organized!** After submission of your first design project, your sub-folder should look like this:

```
yournetid
│   01_report.pdf
└───01_code
│   │   GenerateResults.ipynb
│   │   ae353-cmg.py
│   └───urdf
│       │   checker_blue.png
│       │   cmg.urdf
│       │   cmg_inner.stl
│       │   cmg_outer.stl
│       │   cmg_wheel.stl
│       │   plane.mtl
│       │   plane.obj
│       │   plane.urdf
|       ...
```

You are welcome to resubmit your report at any time. To do so, please **replace** your existing report. Please do not create new reports or move old ones to `01_report_old.pdf` or anything like that.

### Evaluation

We will look at your submissions in the order that they are received. Early submissions are strongly encouraged. We will provide written feedback but will provide only one of three possible grades:

* Not satisfactory for B
* Satisfactory for B
* Better than B

We will only distinguish between grades higher than B when we look at your entire portfolio of project work at the end of the semester.

To improve your portfolio, you are welcome (but not required) to resubmit your video, code, and/or report after receiving our written feedback anytime before the last day of class (May 5, 2021).

### Frequently asked questions

#### Must I submit drafts prior to the March 1 deadline?

No. You are welcome to submit the final version of your project early, though! You are also welcome to revise and resubmit your video, code, and/or report after receiving our written feedback anytime before the last day of class (see [Evaluation](#evaluation)).

#### May I watch videos that are submitted by other students?

Yes. All videos will be available in the [AE353 (Spring 2021) Project Videos](https://mediaspace.illinois.edu/channel/channelid/201808523) channel on Illinois Media Space as soon as they are submitted by your colleagues (see the [Video](#video) deliverable). You may watch these videos whenever you want, even before you submit your own.

If you are inspired by a video, or if watching a video strongly influences the way you proceed with your own design project, then you must **acknowledge and cite** this video in your report (and in your own video, if appropriate). Failure to do so would be considered [plagiarism](https://studentcode.illinois.edu/article1/part4/1-402/).

#### May I read code and reports that are submitted by other students?

Yes. Although you are only an "Editor" of your own sub-folder (see the [Report](#report) deliverable), you are a "Previewer" of all other sub-folders on Box in the [AE353 (Spring 2021) Project Submissions](https://uofi.box.com/s/56ieq301xo6dp334j2hbsr2ypvqebjku) folder. You may look at the code and read the reports of any other student whenever you want, even before you submit your own.

If you are inspired by the report **or the code** of another student, or if looking at this material strongly influences the way you proceed with your own design project, then you must **acknowledge and cite** these sources in your own report. Failure to do so would be considered [plagiarism](https://studentcode.illinois.edu/article1/part4/1-402/).

#### May I work together with other students?

You must submit your own video, code, and report. You must have created them yourself and must **acknowledge and cite** any sources that strongly influenced you, including the materials submitted by your colleagues.

You are encouraged to discuss the project with your colleagues and, in any case, are always able to watch the videos, look at the code, and read the reports that are submitted by other students (see the questions about [watching videos](#may-i-watch-videos-that-are-submitted-by-other-students) and [reading code or reports](#may-i-read-code-and-reports-that-are-submitted-by-other-students)).

#### How do I get started?

The first thing you should do is [download the code]({{ site.github.repository_url }}), verify that you can run the simulation, and mess around a little bit with different actuator commands (e.g., constant torques applied to the gimbal and the rotor) to get a sense for how the system responds. You might want to try a PD controller, as we did in the first couple weeks of class, even before you start doing any analysis.

After that, if you have read the entire [project description](#design-project-1) and are not sure how to proceed, then take your best guess and ask a question on [Campuswire](https://campuswire.com/c/GC4DB42F3). Improving your ability to get unstuck by asking a good question is an explicit goal of this course.

#### What is "the model" that I should linearize?

As we saw in [Week 3](schedule#week-3), the standard way to produce a state space model is to linearize a set of ODEs that describe the equations of motion. You will find ODEs that describe the equations of motion for the CMG system in [the system](#the-system) section above. If you are interested, the [derivation of these ODEs]({{ site.github.repository_url }}/blob/main/projects/01_cmg/DeriveEOM.ipynb) has also been provided for you. I would start with these ODEs.

You will quickly realize that it may be a good idea to restrict your attention only to the platform and the gimbal, treating the rotor as a source of torque (similar to how we handled the platform example in class on [Day 09](schedule#day-09-linearization-friday-february-12)). In particular, for the purpose of control design and analysis, you may want to assume that the angular velocity of the rotor is constant and to completely ignore the second-order ODE that describes how this rotor responds to applied torque.

It is entirely up to you how to proceed, though. There is no one right answer.



# Running Class Code

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
  - sympy
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


## Using Github
There are three main ways to access a local copy of the Class Code, which is stored in the Github repository.  The first way is to navigate to the class Github repository click on the green code button and select 'Download Zip'.  This will provide you with a ZIP file of the class code, which can be run on your personal machine.  Now you might be saying, that is great but I don't want to download a new ZIP file every time something changes.  In that case you want a local copy of the class Github repository.  You should use on the the two following methods to accomplish this.

### Using Github with a Clone
A clone is a copy of a repository.  You are free to make changes to the repository and will be able to get an up to date version of the original repository.
To clone the class repository simply click the green **Code** button in the header of the repository and copy the url presented to you for cloning ```https://github.com/tbretl/ae353-sp21.git```. Make sure you have Git installed on your computer (if not view instructions below under Install Git client tools) and then git bash into the directory where you want to store the local copy of the repository.  Then run the following commands.
```
git clone https://github.com/tbretl/ae353-sp21.git
``` 
The class repository will then be copied into the directory.

To update the class repository you have a two options: ```fetch``` and ```pull```.

* Fetching will retrieve all the new work in the class repository, but will not merge those changes into your local repository.  This means that your work will not be overwritten.  To fetch simply git bash into the repo directory and run the command ```git fetch origin```.
* After fetching you can run ```git merge main```, where main is the name of the branch.
* As a shortcut you can run the ```git pull origin``` command which will complete both fetch and merge.

### Using Github with a Fork
A fork of the repository is a copy of the repository.  You are free to experiment with your local copy without fear of affecting the original repository.  A fork is useful because unlike a clone, there is still a link between the original repository and your local copy.  This means that you can contribute to the class code by using Pull Requests.

To fork the class repository simply click the **Fork** button in the header of the repository.  This will allow you to create a forked repository on your own Github account.
Now perhaps you want to be able to access this repository from your computer, no worries.  Make sure you have Git installed on your computer (if not view instructions below under Install Git client tools) and then git bash into the directory where you want to store the local copy of the repository.  Then run the following commands.
```
git clone https://github.com/<GITHUB USERNAME>/<REPOSITORY NAME>.git

git remote add upstream https://github.com/tbretl/ae353-sp21.git

git fetch upstream
```

* Be sure to replace <GITHUB USERNAME> with your Github Username and <REPOSITORY NAME> with the name of the repository, probably ae353-sp21.

Now confirm that you have defined the remote copy of the repository correctly by running `git remote -v`.  The output should look something like this.

```
origin  https://github.com/<GITHUB USERNAME>/ae353-sp21 (fetch)
origin  https://github.com/<GITHUB USERNAME>/ae353-sp21 (push)
upstream        https://github.com/tbretl/ae353-sp21 (fetch)
upstream        https://github.com/tbretl/ae353-sp21 (push)
```

If you made a mistake, you can remove the remote value. To remove the upstream value, run the command `git remote remove upstream`.


### Install Git client tools

Install the latest version of Software Freedom Conservancy's Git client tools for your platform.

* [Git for Windows](https://git-scm.com/download/win). This install includes the Git version control system and Git Bash, the command-line app that you use to interact with your local Git repository.
* Git for Mac is provided as part of the Xcode Command Line Tools. Simply run git from the command line. You will be prompted to install the command line tools if needed. You can also download [Git for Mac](https://git-scm.com/download/mac) from the Software Freedom Conservancy.
* [Git for Linux and Unix](https://git-scm.com/download/linux)


### Shortcut to running Class Code

If you are sick of having to use the terminal to run the class code, you can create a small program called a bash script to do it for you.

#### On Windows
Open Notepad or a text editor of your choice and paste the following lines of code.  Then change the top two paths: the CONDA PATH, the path to your installation of Miniconda or Anacoda, and the CLASSCODE PATH, the path to your local copy of the class code repository.  If you called your ae353 environment something different, you should change it here as well by changing the ENVNAME variable.  Next save the batch script as something like ```runClassCode.bat``` and save it in your desired location.  When you double click the script, it will open a terminal and run all the necessary commands for you and will open up a jupyter notebook in the directory housing your local copy of the class code repository.  If seeing some lines of code popping up on the terminal makes you nervous, no worries, simply remove the ```rem``` before ```@echo OFF``` in the first line of your batch script.

```
rem @echo OFF

rem Define here the path to your conda installation
set CONDAPATH=C:\Users\<USERNAME>\Anaconda3
rem Define here the name of the environment
set ENVNAME=ae353-bullet
rem Define here the path to the class code
set CLASSCODEPATH=C:\Users\<USERNAME>\AE 353 - Aerospace Control Systems\Class Code\ae353-sp21


rem CHANGE THE CODE BELOW THIS LINE AT YOUR OWN RISK.

cd %CLASSCODEPATH%

if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)


call %CONDAPATH%\Scripts\activate.bat %ENVPATH%

rem Run Jupyter Notebook in that environment
jupyter notebook

rem Deactivate the environment
call conda deactivate
```
#### On Mac or Linux
You can do accomplish the same task by creating a .sh file.




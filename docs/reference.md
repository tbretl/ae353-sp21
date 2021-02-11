---
layout: default
title: Reference
tagline: An invitation to aerospace control
description: Supplementary notes and other reference material
---

## Contents
{:.no_toc}

* This text will be replaced by a table of contents (excluding the above header) as an unordered list
{:toc}

---

## State space models

A **state-space model** has this form:

$$
\begin{aligned}
\dot{x} &= Ax + Bu \\
y &= Cx + Du
\end{aligned}
$$

There are three variables:

* $x$ is the **state**
* $u$ is the **input**
* $y$ is the **output**

All three variables are functions of time, so we could have written $x(t)$, $u(t)$, and so forth --- but in general, we won't use that notation unless we need it. We use dots to indicate time derivatives, so $\dot{x}$ means $dx/dt$.

The state, input, and output may have more than one element --- that is to say, they may be vectors (represented by a matrix of numbers) and not scalars (represented by a single number). Suppose, in particular, that:

* the state $x$ has $n_x$ elements
* the input $u$ has $n_u$ elements
* the output $y$ has $n_y$ elements

Then, we would represent them as column matrices:

$$
x =
\begin{bmatrix}
x_1 \\ \vdots \\ x_{n_x}
\end{bmatrix}
\qquad
u =
\begin{bmatrix}
u_1 \\ \vdots \\ u_{n_u}
\end{bmatrix}
\qquad
y =
\begin{bmatrix}
y_1 \\ \vdots \\ y_{n_y}
\end{bmatrix}
$$

Taking the time derivative of a matrix is equivalent to taking the time derivative of each element of that matrix, so we would write

$$
\dot{x} =
\begin{bmatrix}
\dot{x}_1 \\ \vdots \\ \dot{x}_{n_x}
\end{bmatrix}
$$

The state-space model also has four constants: $A$, $B$, $C$, and $D$. If $x$, $y$, and $u$ are column matrices with (possibly) more than one element, then these constants have to be matrices as well:

* $A$ is a constant matrix of size $n_x \times n_x$
* $B$ is a constant matrix of size $n_x \times n_u$
* $C$ is a constant matrix of size $n_y \times n_x$
* $D$ is a constant matrix of size $n_y \times n_u$

The first part of a state space model is a set of $n_x$ ordinary differential equations that describe the dynamics of a system:

$$\dot{x} = Ax + Bu$$

The second part of a state space model is a set of $n_y$ purely algebraic equations that describe how sensor measurements or other quantities of interest are related to state and input variables:

$$y = Cx + Du$$

The state-space model has two key properties:

* it is **linear** because both $\dot{x}$ and $y$ are linear functions of $x$ and $u$
* it is **time-invariant** because $A$, $B$, $C$, and $D$ are constant

<div class="alert alert-warning">
Other people use other symbols for both the variables and constants in a state space model. Indeed, we will sometimes use other symbols for these things as well. For example:

$$
\begin{aligned}
\dot{z} &= Ez + Fv \\
w &= Gz + Hv
\end{aligned}
$$

This is also a "state space model," in which the state is $z$, the input is $v$, and the output is $w$.
</div>

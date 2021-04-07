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

### What is a state space model?

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

The state space model has two key properties:

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


### How do I put a system in state space form?

Suppose we are given a description of a dynamic system and of sensor measurements or other quantities of interest.
We would like to describe this same system with a state space model.

Remember that every state space model is linear. The equations of motion that describe a dynamic system are often nonlinear. So apparently, we will have to accept that state space models can only *approximate* some of the systems we want to describe.

We will use **linearization** to arrive at this approximation, in four steps.

**Step 1.** Rewrite the system as a set of first-order ordinary differential equations:

$$
\begin{aligned}
\dot{m} &= f(m,n) \\
z &= g(m,n)
\end{aligned}
$$

In this expression, the variables $m$, $n$, and $z$ are functions of time and can have more than one element --- in general, you should represent them as column matrices. As we said before, the functions $f(\cdot)$ and $g(\cdot)$ will often be nonlinear.

**Step 2.** Find an equilibrium point $m_{e}, n_{e}$ of the system by solving this equation:

$$
0 = f(m_{e},n_{e})
$$

A solution to this equation is called an equilibrium point because if

$$m = m_e \qquad n = n_e$$

then

$$\dot{m} = f(m_e, n_e) = 0$$

and so $m$ remains constant. That is to say, if the system reaches an equilibrium point, then it stays there. This is an important property! The goal of almost every controller we design in this course will be to make a system reach an equilibrium point quickly and reliably.

This equation may have no solutions, in which case no equilibrium point exists for the system. This is bad. We will ignore this situation for now.

This equation also may have many solutions, in which case you have to make a choice. A good choice is whatever equilibrium point you would like your system to achieve.

**Step 3.** Define the state, input, and output as follows:

$$
x = m-m_{e}
\qquad
u = n-n_{e}
\qquad
y = z-g(m_{e},n_{e})
$$

Note that $x$ measures *error* --- the *difference* between $m$ and its equilibrium value. When error is zero, the system has reached equilibrium and is doing what we want. Apparently, with this way of defining the state and the input, "control design" means choosing $u$ so that $x$ goes to zero.

**Step 4.** Compute $A$, $B$, $C$, and $D$ as follows:

$$
A = \frac{\partial f}{\partial m}\biggr\rvert_{(m_{e},n_{e})}
\qquad
B = \frac{\partial f}{\partial n}\biggr\rvert_{(m_{e},n_{e})}
\qquad
C = \frac{\partial g}{\partial m}\biggr\rvert_{(m_{e},n_{e})}
\qquad
D = \frac{\partial g}{\partial n}\biggr\rvert_{(m_{e},n_{e})}
$$

<div class="alert alert-warning">
Recall that

$$
\frac{\partial f}{\partial m}\biggr\rvert_{(m_{e},n_{e})}
$$

is the <a href="https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant">Jacobian (i.e., matrix of partial derivatives)</a> of $f$ with respect to $m$, evaluated at the equilibrium point.
</div>

Why does this make any sense? Look again at the ODEs that describe the original system:

$$\dot{m} = f(m, n)$$

First, because

$$x = m - m_e$$

then

$$\dot{x} = \dot{m} - 0 = \dot{m}$$

So the *left*-hand side of the ODEs can simply be replaced with $\dot{x}$.

Now, suppose we want a linear approximation to the *right*-hand side of the ODEs --- the function $f(m, n)$. One way to find such an approximation is to take a [Taylor's series expansion](https://en.wikipedia.org/wiki/Taylor_series) about $m_e, n_e$ up to first order:

$$
\begin{aligned}
f(m, n)
&\approx f(m_e, n_e) + \frac{\partial f}{\partial m}\biggr\rvert_{(m_{e},n_{e})} \left( m - m_e \right) + \frac{\partial f}{\partial n}\biggr\rvert_{(m_{e},n_{e})} \left( n - n_e \right) \\
&= 0 + A x + B u \\
&= A x + B u
\end{aligned}
$$

There you have it: "$\dot{x} = Ax + Bu$" is a first-order (i.e., linear) approximation to "$\dot{m} = f(m, n)$".


#### Example (first-order)

Consider the system with dynamics

$$\dot{\omega} + 2 \omega = \tau$$

and measurement

$$\gamma = \omega$$

Let's apply our method to put this system in state space form.

We begin by rewriting it as a set of first-order ODEs. Lucky us, the system is already described by just one first-order ODE, so all we need to do is solve for $\dot{w}$:

$$
\begin{aligned}
\dot{\omega} &= f(\omega, \tau) = -2\omega + \tau \\
\gamma &= g(\omega, \tau) = \omega
\end{aligned}
$$

Next, we find an equilibrium point by solving

$$0 = -2 \omega_e + \tau_e$$

In this case, there are many solutions. Suppose we pick this one:

$$\omega_e = 10 \qquad \tau_e = 20$$

Then, we define the state, input, and output based on this choice of equilibrium point:

$$x = \omega - \omega_e \qquad u = \tau - \tau_e \qquad y = \gamma - \omega_e$$

Finally, we compute $A$, $B$, $C$, and $D$ by taking Jacobians (easy in this case because all the variables are scalars):

$$
\begin{aligned}
A &= \frac{\partial \left(-2\omega + \tau\right)}{\partial \omega}\biggr\rvert_{(\omega_{e},\tau_{e})} = -2
&&
B = \frac{\partial \left(-2\omega + \tau\right)}{\partial \tau}\biggr\rvert_{(\omega_{e},\tau_{e})} = 1 \\[1em]
C &= \frac{\partial \left(\omega\right)}{\partial \omega}\biggr\rvert_{(\omega_{e},\tau_{e})} = 1
&&
D = \frac{\partial \left(\omega\right)}{\partial \tau}\biggr\rvert_{(\omega_{e},\tau_{e})} = 0
\end{aligned}
$$

The resulting state space model is

$$
\begin{aligned}
\dot{x} &= Ax + Bu && = -2x + u \\
y &= Cx + Du && = x
\end{aligned}
$$

Note that the original system was linear, so there was no approximation here. We could probably have skipped most of these steps and written the system in state-space form by inspection. On the other hand, it is nice to know that the process of "linearization" still works even in this simple case.


#### Example (second-order)

Consider the system with dynamics

$$\ddot{q} + 3 \sin q = \tau$$

and measurement

$$\gamma = \cos{q}$$

Let's apply our method to put this system in state-space form.

We begin by rewriting it as a set of first-order ODEs:

* We find the time-derivative of $q$ with highest order --- in this case, $\ddot{q}$, of order 2.
* We define *new variables* for each time-derivative of $q$ with lower order --- in this case, $\dot{q}$, the only time-derivative with order between 0 and 2. We might choose the following name for this time-derivative:

$$ v = \dot{q} $$

* We rewrite the original ODEs (in this case, just one) in terms of these new variables:

$$\dot{v} + 3\sin q = \tau$$

* We add one extra ODE for each new variable (in this case, just one extra) --- this is trivial, coming from the way we defined these new variables:

$$\dot{q} = v$$

* We collect the original ODEs and the extra ODEs together, if necessary solving for all of the time-derivatives (that's not necessary here):

$$
\begin{aligned}
\dot{q} &= v \\
\dot{v} &= -3\sin q + \tau
\end{aligned}
$$

* Finally, we rewrite our result in the form $\dot{m} = f(m, n)$ by collecting things in column matrices as follows:

$$\begin{bmatrix} \dot{q} \\ \dot{v} \end{bmatrix} = \begin{bmatrix} v \\ -3\sin q + \tau \end{bmatrix}$$

Note that, as desired, these rewritten ODEs have time derivatives that are at most of first order. Also note that all of these time-derivatives are on the left-hand side of the equations --- none appear on the right-hand side.

Next, we find an equilibrium point by solving

$$\begin{bmatrix} 0 \\ 0 \end{bmatrix} = \begin{bmatrix} v \\ -3\sin q + \tau \end{bmatrix}$$

There are many solutions. Suppose we pick this one:

In this case, there are many solutions. Suppose we pick this one:

$$q_e = \pi / 2 \qquad v_e = 0 \qquad \tau_e = 3$$

Then, we define the state, input, and output based on this choice of equilibrium point:

$$x = \begin{bmatrix} q - q_e \\ v - v_e \end{bmatrix} \qquad u = \begin{bmatrix}\tau - \tau_e\end{bmatrix} \qquad y = \begin{bmatrix}\gamma - \cos{q_e}\end{bmatrix}$$

Finally, we compute $A$, $B$, $C$, and $D$ by taking Jacobians. We will show our work for $A$ in detail:

$$
\begin{aligned}
A
&= \frac{\partial f}{\partial \begin{bmatrix} q \\ v \end{bmatrix}}\biggr\rvert_{\left(\begin{bmatrix}q_e\\v_e\end{bmatrix},\begin{bmatrix}\tau_{e}\end{bmatrix}\right)} \\
&= \left.\begin{bmatrix} \dfrac{\partial(v)}{\partial q} & \dfrac{\partial(v)}{\partial v} \\ \dfrac{\partial(-3\sin q + \tau)}{\partial q} & \dfrac{\partial(-3\sin q + \tau)}{\partial v} \end{bmatrix}\right\rvert_{\left(\begin{bmatrix}q_e\\v_e\end{bmatrix},\begin{bmatrix}\tau_{e}\end{bmatrix}\right)} \\
&= \left.\begin{bmatrix} 0 & 1 \\ -3\cos q & 0 \end{bmatrix}\right\rvert_{\left(\begin{bmatrix}q_e\\v_e\end{bmatrix},\begin{bmatrix}\tau_{e}\end{bmatrix}\right)} \\
&= \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}
\end{aligned}
$$

We simply state our results for the other coefficient matrices:


$$
B = \begin{bmatrix} 0 \\ 1 \end{bmatrix} \qquad
C = \begin{bmatrix} 1 & 0 \end{bmatrix} \qquad
D = \begin{bmatrix} 0 \end{bmatrix}
$$

The resulting state space model is

$$
\begin{aligned}
\dot{x} &= Ax + Bu && = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}x + \begin{bmatrix} 0 \\ 1 \end{bmatrix}u \\[1em]
y &= Cx + Du && = \begin{bmatrix} 1 & 0 \end{bmatrix}x + \begin{bmatrix} 0 \end{bmatrix}u
\end{aligned}
$$

The original system was nonlinear and the state space model is linear, so there *must* be some approximation here! As we will see, this approximation is good near the equilibrium point but can be very bad elsewhere.


# The matrix exponential function

## What is the matrix exponential?

The **matrix exponential** of a square matrix $M$ is the infinite series

$$
e^M = I + M + \frac{1}{2}M^2 + \frac{1}{6}M^3 + \dotsm = \sum_{k=0}^{\infty} \dfrac{1}{k !} M^k
$$

where $I$ is the identity matrix. This series converges for any square matrix $M$.


## How do I use the matrix exponential to solve a linear system?

The solution to the set of linear ODEs

$$ \dot{x} = Fx $$

with the initial condition

$$ x(t_0) = x_0 $$

is

$$ x(t) = e^{F (t - t_0)} x_0. $$

How do we know that this solution is correct? First, let's check that this solution satisfies the ODEs:

$$
\begin{aligned}
\dot{x}
&= \frac{d}{dt} \left( e^{F (t - t_0)} x_0 \right) \\
&= \frac{d}{dt} \left( \left( I + F(t-t_0) + \frac{1}{2} F^2(t-t_0)^2 + \frac{1}{6} F^2(t-t_0)^3 + \dotsm \right) x_0 \right) \\
&= \frac{d}{dt} \left( I + F(t-t_0) + \frac{1}{2} F^2(t-t_0)^2 + \frac{1}{6} F^3(t-t_0)^3 + \dotsm \right) x_0 \\
&= \left( \frac{d}{dt} \left( I \right) + \frac{d}{dt} \left( F(t-t_0) \right) + \frac{d}{dt} \left( \frac{1}{2} F^2(t-t_0)^2 \right) + \frac{d}{dt} \left( \frac{1}{6} F^3(t-t_0)^3 \right) \dotsm \right) x_0 \\
&= \left( 0 + F + F^2(t-t_0) + \frac{1}{2} F^3(t-t_0) + \dotsm \right) x_0 \\
&= F \left(I + F(t-t_0) + \frac{1}{2} F^2(t-t_0)^2 + \dotsm \right) x_0 \\
&= F e^{F(t-t_0)} x_0
\end{aligned}
$$

Apparently, it does. Second, let's check that this solution satisfies the initial condition:

$$ \begin{aligned} x(t_0) &= e^{F(t_0 - t_0)} x_0 \\ &= e^0 x_0 \\ &= I x_0 \\ &= x_0 \end{aligned} $$

Again, it does. (We might wonder if this is the *only* solution to the original ODEs --- it is, although a proof would require more work.)

## How do I use the matrix exponential to solve state space models?

Consider the state space model

$$ \dot{x} = Ax + Bu$$

This model does not look the same as

$$ \dot{x} = Fx $$

Indeed, without specifying $u$, we cannot solve for $x$ as a function of time. However, particular choices of $u$ allow us to simplify the state space model. For example, if we choose $u = 0$, then we can write

$$ \begin{aligned} \dot{x} &= Ax+Bu \\ &= Ax + B \cdot (0) \\ &= Ax + 0 \\ &= Ax \end{aligned} $$

and so we are right back at a linear system that can be solved with the matrix exponential. Another common choice of $u$ is

$$ u = -Kx $$

for some constant matrix $K$. (What would the size of $K$ have to be for us to define $u$ in this way?) This choice of $u$ is called **state feedback**, since the input depends on the state. If we plug this choice into our state space model, then we can write

$$
\begin{aligned}
\dot{x} &= Ax + Bu \\
&= Ax + B(-Kx) \\
&= (A - BK) x
\end{aligned}
$$

and so --- just like before --- we are right back at a linear system that can be solved with the matrix exponential. Although this result will get us a long way, we will see how to solve state space models for other choices of input later on.

# Asymptotic stability

## What are eigenvalues and eigenvectors?

Consider a square matrix $F \in \mathbb{R}^{n \times n}$. If we can find a complex number $s \in \mathbb{C}$ and a non-zero, complex-valued vector $v \in \mathbb{C}^n$ that satisfy

$$ (s I - F) v = 0 $$

then we call $s$ an **eigenvalue** of $F$ and $v$ the corresponding **eigenvector** of $F$. If we wanted, we could rearrange this equation to put it in a form that might be more familiar:

$$ 0 = (s I - F) v = s v - F v \qquad\Rightarrow\qquad F v = s v. $$

One way to find eigenvalues is to solve the equation

$$ \det (s I - F) = 0 $$

where "$\det(\cdot)$" means taking a determinant. In general, this equation will be an $n$th-order polynomial in $s$, and so will have $n$ solutions --- we might call them $s_1, \dotsc, s_n$. To find an eigenvector that corresponds to each eigenvalue $s_i$, we solve

$$ F v_i = s_i v_i $$

for $v_i$. Note that there are many possible solutions to this equation and that eigenvectors are only unique up to a scale factor. In particular, for any real number $k \in \mathbb{R}$, we have

$$ \begin{aligned} F (k v_i) &= k (F v_i) \\ &= k (s v_i) \\ &= s (k v_i). \end{aligned}$$

Apparently, if $v_i$ is an eigenvector corresponding to $s_i$, then so is $k v_i$ for any $k \neq 0$. For this reason, algorithms to find eigenvectors typically *normalize* them to have unit length.

## How do I diagonalize a square matrix?

Suppose we have found the eigenvalues $s_1, \dotsc, s_n$ and eigenvectors $v_1, \dotsc, v_n$ of a square matrix $F\in\mathbb{R}^{n \times n}$. Define the matrix

$$V = \begin{bmatrix} v_1 & \dotsm & v_n \end{bmatrix}$$

with an eigenvector in each column, and also the matrix

$$\text{diag} (s_1, \dotsc, s_n) = \begin{bmatrix} s_1 & 0 & \dotsm & 0 \\ 0 & s_2 & \dotsm & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dotsm & s_n \end{bmatrix}$$

with the eigenvalues along the diagonal.

Two things are true.

First, the following equality holds:

$$F V = V \text{diag} (s_1, \dotsc, s_n) $$

You could easily verify this result for yourself.

Second, if $s_1, \dotsc, s_n$ are all *distinct* (i.e., if no two eigenvalues are the same), then the matrix $V$ is *invertible*. This result is harder to verify --- it has to do with the fact that if the eigenvalues are distinct then the eigenvectors are linearly independent.

The key consequence of $V$ being invertible is that we can solve the above equality to write:

$$\text{diag} (s_1, \dotsc, s_n) = V^{-1} F V.$$

In this case --- if all eigenvalues are distinct and so the matrix of eigenvectors is invertible --- we say that $F$ is **diagonalizable**. The process of "diagonalizing $F$" is finding the matrix $V$.

## What is the matrix exponential of a diagonal matrix?

It is easy to find the matrix exponential of a diagonal matrix, starting from [the definition](#what-is-the-matrix-exponential):

$$
\begin{align*}
e^{\text{diag} (s_1, \dotsc, s_n)t}
&= I + \text{diag} (s_1, \dotsc, s_n)t + \frac{1}{2}\left( \text{diag} (s_1, \dotsc, s_n) t \right)^2 + \dotsm \\
&=
\begin{bmatrix} 1 & 0 & \dotsm & 0 \\ 0 & 1 & \dotsm & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dotsm & 1 \end{bmatrix}
+
\begin{bmatrix} s_1t & 0 & \dotsm & 0 \\ 0 & s_2t & \dotsm & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dotsm & s_nt \end{bmatrix}
+
\begin{bmatrix} (s_1t)^2/2 & 0 & \dotsm & 0 \\ 0 & (s_2t)^2/2 & \dotsm & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dotsm & (s_nt)^2/2 \end{bmatrix}
+ \dotsm \\
&= \begin{bmatrix} 1 + s_1t + (s_1t)^2/2 + \dotsm & 0 & \dotsm & 0 \\ 0 & 1 + s_2t + (s_2t)^2/2 + \dotsm & \dotsm & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dotsm & 1 + s_nt + (s_nt)^2/2 + \dotsm \end{bmatrix} \\
&= \begin{bmatrix} e^{s_1t} & 0 & \dotsm & 0 \\ 0 & e^{s_2t} & \dotsm & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dotsm & e^{s_nt} \end{bmatrix}
\end{align*}
$$

## What is the solution to a linear system that is diagonalizable?

[We have seen](#how-do-i-use-the-matrix-exponential-to-solve-a-linear-system) that the solution to

$$\dot{x} = Fx$$

with the initial condition

$$x(0) = x_0$$

is

$$x(t) = e^{Ft}x_0.$$

Suppose $F$ is a diagonalizable matrix, so that

$$\text{diag} (s_1, \dotsc, s_n) = V^{-1} F V$$

where

$$\text{diag} (s_1, \dotsc, s_n)$$

is a diagonal matrix that contains the eigenvalues of $F$ and where

$$V = \begin{bmatrix} v_1 & \dotsm & v_n \end{bmatrix}$$

is a matrix of the corresponding eigenvectors. Then, applying [the definition of matrix exponential](#what-is-the-matrix-exponential) again, we have

$$
\begin{align*}
e^{Ft}x_0
&= e^{V \text{diag} (s_1, \dotsc, s_n) V^{-1}t}x_0 \\
&= \left( I + V \text{diag} (s_1, \dotsc, s_n) V^{-1}t + \frac{1}{2}\left( V \text{diag} (s_1, \dotsc, s_n) V^{-1}t \right)^2 + \dotsm\right) x_0 \\
&= V \left( I + \text{diag} (s_1, \dotsc, s_n) t + \frac{1}{2} \left( \text{diag} (s_1, \dotsc, s_n)t \right)^2 + \dotsm\right) V^{-1}x_0 \\
&= V e^{\text{diag} (s_1, \dotsc, s_n)t}V^{-1}x_0 \\
&= V \begin{bmatrix} e^{s_1t} & 0 & \dotsm & 0 \\ 0 & e^{s_2t} & \dotsm & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dotsm & e^{s_nt} \end{bmatrix} V^{-1}x_0
\end{align*}
$$

where the last step comes from what we just found out about the [matrix exponential of a diagonal matrix](#what-is-the-matrix-exponential-of-a-diagonal-matrix). In this expression, the terms $V$, $V^{-1}$, and $x_0$ are constant. The only terms that depend on $t$, in fact, are the *scalar* exponential functions

$$e^{s_1t}, \dotsc, e^{s_nt}$$

that appear in the diagonal of

$$e^{\text{diag} (s_1, \dotsc, s_n)t}.$$

Therefore, we can infer the behavior of $x(t)$ based entirely on these scalar exponential functions. In particular, suppose that each eigenvalue $s_i$ — a complex number — has real part $a_i$ and imaginary part $b_i$, or in other words that

$$s_i = a_i + jb_i.$$

[Euler's formula](https://en.wikipedia.org/wiki/Euler%27s_formula) tells us that

$$e^{s_it} = e^{(a_i+jb_i)t} = e^{a_it}\left(\cos(b_it) + j\sin(b_it)\right).$$

Apparently, as time gets large, one of three things is true about each of these terms:

* if $a_i > 0$, then $e^{(a_i+jb_i)t}$ grows quickly
* if $a_i = 0$, then $e^{(a_i+jb_i)t}$ is constant ($b_i=0$) or is sinusoidal with constant magnitude ($b_i \neq 0$)
* if $a_i < 0$, then $e^{(a_i+jb_i)t}$ decays quickly to zero

It is possible to show that (more or less) the same result holds for *any* system $\dot{x}=Fx$, not only ones for which $F$ is diagonalizable. This takes more work, and involves the transformation of $F$ into [Jordan normal form](https://en.wikipedia.org/wiki/Jordan_normal_form) rather than into a diagonal matrix. We would discover that the terms that depend on $t$ all look like

$$t^me^{s_it}$$

where $m$ is an integer that is at most the multiplicity of the eigenvalue $s_i$. Since $e^{a_it}$ increases or decreases a lot faster than $t^m$, then the same three things we listed above would be true of each term in $x(t)$, just like before.

See [the reference textbook](https://fbswiki.org/) for details.

## When is a linear system asymptotically stable?

The system

$$\dot{x} = Fx$$

is called **asymptotically stable** if $x(t) \rightarrow 0$ as $t \rightarrow \infty$, starting from any initial condition $x(t_0) = x_0.$

Based on our observations about [the solution to linear systems that are diagonalizable](#what-is-the-solution-to-a-linear-system-that-is-diagonalizable), we can state the following important result:

<div class="alert alert-warning">
The system

$$\dot{x} = Fx$$

is asymptotically stable if and only if all eigenvalues of $F$ have negative real part.
</div>

In particular, we now have a test for whether or not a controller "works." Suppose we apply linear state feedback

$$u = -Kx$$

to the state space system

$$\dot{x} = Ax + Bu$$

so that

$$\dot{x} = (A - BK)x.$$

The controller "works" when this system is asymptotically stable, i.e., when $x$ goes to zero as time gets large. We now know, therefore, that the controller "works" when all eigenvalues of $A - BK$ have negative real part.

We may not have a systematic way of *finding* a matrix $K$ to make the closed-loop system stable yet, but we certainly do have a systematic way now of deciding whether or not a *given* matrix $K$ makes the closed-loop system stable.

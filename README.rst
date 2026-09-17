========
llvmlite
========

Infernux maintenance fork
------------------------

This is an upstream-derived dependency of the
`Infernux game engine <https://github.com/ChenlizheMe/Infernux>`_'s CPU JIT work.
It is not a Taichi backend or an Infernux plugin. The original llvmlite API,
copyright notices and license remain in place; upstream documentation follows.

The changes here repair native optimization-pass disposal and release the
instrumentation callbacks owned by each PassBuilder. Regression tests check
that closing a pass manager invokes its native destructor exactly once.
MCJIT engines also expose ``memory_statistics``: current and peak mapped bytes
for code/data pages, including allocator padding. Both existing memory-manager
choices retain their allocation behavior; the counters follow the engine's
lifetime without a process-global tracking table. These are not total RSS or
compiler IR measurements. The original C creation entry point is retained.
These fixes do not by themselves implement an executable-code memory budget.
Infernux's dispatcher retirement work is separate. The fork is not yet the
dependency installed by the public Infernux wheel.

这是 `Infernux 游戏引擎 <https://github.com/ChenlizheMe/Infernux>`_ 为 CPU JIT
维护的 llvmlite 分支，不是插件，也不参与 Taichi 的 Vulkan 编译路径。
当前修改针对 LLVM 优化资源的释放问题，保留上游 API、版权与许可证。
MCJIT 新增实际代码/数据映射页的当前与峰值字节统计，包含分配器对齐开销；
沿用现有两种内存管理器，不另建全局对象表。统计不等于进程总内存或编译器 IR 占用。
这些修复不等于完整的机器码内存管理已经完成；公开的引擎 wheel 暂未切换到此分支。

Upstream: `numba/llvmlite <https://github.com/numba/llvmlite>`_.

.. image:: https://dev.azure.com/numba/numba/_apis/build/status/numba.llvmlite?branchName=main
   :target: https://dev.azure.com/numba/numba/_build/latest?definitionId=2&branchName=main
   :alt: Azure Pipelines
.. image:: https://coveralls.io/repos/github/numba/llvmlite/badge.svg
   :target: https://coveralls.io/github/numba/llvmlite
   :alt: Coveralls.io
.. image:: https://readthedocs.org/projects/llvmlite/badge/
   :target: https://llvmlite.readthedocs.io
   :alt: Readthedocs.io

A Lightweight LLVM Python Binding for Writing JIT Compilers
-----------------------------------------------------------

.. _llvmpy: https://github.com/llvmpy/llvmpy

llvmlite is a project originally tailored for Numba_'s needs, using the
following approach:

* A small C wrapper around the parts of the LLVM C++ API we need that are
  not already exposed by the LLVM C API.
* A ctypes Python wrapper around the C API.
* A pure Python implementation of the subset of the LLVM IR builder that we
  need for Numba.

Why llvmlite
============

The old llvmpy_  binding exposes a lot of LLVM APIs but the mapping of
C++-style memory management to Python is error prone. Numba_ and many JIT
compilers do not need a full LLVM API.  Only the IR builder, optimizer,
and JIT compiler APIs are necessary.

Key Benefits
============

* The IR builder is pure Python code and decoupled from LLVM's
  frequently-changing C++ APIs.
* Materializing a LLVM module calls LLVM's IR parser which provides
  better error messages than step-by-step IR building through the C++
  API (no more segfaults or process aborts).
* Most of llvmlite uses the LLVM C API which is small but very stable
  (low maintenance when changing LLVM version).
* The binding is not a Python C-extension, but a plain DLL accessed using
  ctypes (no need to wrestle with Python's compiler requirements and C++ 11
  compatibility).
* The Python binding layer has sane memory management.
* llvmlite is faster than llvmpy thanks to a much simpler architecture
  (the Numba_ test suite is twice faster than it was).

Compatibility
=============

llvmlite has been tested with Python 3.10 -- 3.15 and is likely to work with
greater versions.

As of version 0.48.0, llvmlite requires LLVM 22.x.x on all architectures

Historical compatibility table:

=================  ========================
llvmlite versions  compatible LLVM versions
=================  ========================
0.48.0 - ......    22.x.x
0.45.0 - 0.47.x    20.x.x
0.44.0             15.x.x and 16.x.x
0.41.0 - 0.43.0    14.x.x
0.40.0 - 0.40.1    11.x.x and 14.x.x (12.x.x and 13.x.x untested but may work)
0.37.0 - 0.39.1    11.x.x
0.34.0 - 0.36.0    10.0.x (9.0.x for  ``aarch64`` only)
0.33.0             9.0.x
0.29.0 - 0.32.0    7.0.x, 7.1.x, 8.0.x
0.27.0 - 0.28.0    7.0.x
0.23.0 - 0.26.0    6.0.x
0.21.0 - 0.22.0    5.0.x
0.17.0 - 0.20.0    4.0.x
0.16.0 - 0.17.0    3.9.x
0.13.0 - 0.15.0    3.8.x
0.9.0 - 0.12.1     3.7.x
0.6.0 - 0.8.0      3.6.x
0.1.0 - 0.5.1      3.5.x
=================  ========================

Documentation
=============

You'll find the documentation at http://llvmlite.pydata.org


Pre-built binaries
==================

We recommend you use the binaries provided by the Numba_ team for
the Conda_ package manager.  You can find them in Numba's `anaconda.org
channel <https://anaconda.org/numba>`_.  For example::

   $ conda install --channel=numba llvmlite

(or, simply, the official llvmlite package provided in the Anaconda_
distribution)

.. _Numba: http://numba.pydata.org/
.. _Conda: http://conda.pydata.org/
.. _Anaconda: http://docs.continuum.io/anaconda/index.html


Other build methods
===================

If you don't want to use our pre-built packages, you can compile
and install llvmlite yourself.  The documentation will teach you how:
http://llvmlite.pydata.org/en/latest/install/index.html

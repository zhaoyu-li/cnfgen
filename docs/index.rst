.. Entry point document of CNFgen library documentation
   
.. toctree::
   :caption: Table of contents
   :hidden:
   :maxdepth: 2
   :numbered:

   self
   buildcnf
   satsolve
   families
   graphs
   transform
   clitool
   addfamily
   
Welcome to CNFgen's documentation!
==================================

The main components of CNFgen are the ``cnfgen`` library and
the ``cnfgen`` command line utility.

The ``cnfgen`` library
--------------------------

The ``cnfgen``  library is capable to  generate Conjunctive Normal
Form   (CNF)   formulas,   manipulate   them  and,   when   there   is
a satisfiability (SAT) solver properly  installed on your system, test
their satisfiability. The CNFs can be  saved on file in DIMACS format,
which the standard input format for  SAT solvers [1]_, or converted to
LaTeX [2]_  to be included  in a  document. The library  contains many
generators for formulas that  encode various combinatorial problems or
that come from research in Proof Complexity [3]_.

The  main  entry point  for  the  library is  the  :py:class:`cnfgen.CNF`
object. Let's see a simple example of its usage.

   >>> from pprint import pprint
   >>> import cnfgen
   >>> F = cnfgen.CNF()
   >>> F.add_clause([(True,"X"),(False,"Y")])
   >>> F.add_clause([(False,"X")])
   >>> outcome,assignment = F.is_satisfiable() # outputs a pair
   >>> outcome                                 # is the formula SAT?
   True
   >>> pprint(assignment)                      # a solution
   {'X': False, 'Y': False}
   >>> F.add_clause([(True,"Y")])
   >>> F.is_satisfiable()                      # no solution
   (False, None)
   >>> print(F.dimacs(export_header=False))
   p cnf 2 3
   1 -2 0
   -1 0
   2 0
   >>> print(F.latex(export_header=False))
   \begin{align}
   &       \left(            {X} \lor   \overline{Y} \right) \\
   & \land \left(   \overline{X} \right) \\
   & \land \left(            {Y} \right)
   \end{align}

A typical  unsatisfiable formula  studied in  Proof Complexity  is the
pigeonhole principle formula.

   >>> from cnfgen import PigeonholePrinciple
   >>> F = PigeonholePrinciple(5,4)
   >>> print(F.dimacs(export_header=False))
   p cnf 20 45
   1 2 3 4 0
   5 6 7 8 0
   ...
   -16 -20 0
   >>> F.is_satisfiable()
   (False, None)

The ``cnfgen`` command line tool
--------------------------------

The command line  tool is installed along  ``cnfgen`` package, and
provides  a somehow  limited  interface to  the library  capabilities.
It provides ways  to produce formulas in DIMACS and  LaTeX format from
the command line. To produce a  pigeonhole principle from 5 pigeons to
4 holes as in the previous example the command line is

.. code-block:: shell
                
   $ cnfgen php 5 4
   c description: Pigeonhole principle formula for 5 pigeons and 4 holes
   c generator: CNFgen (0.8.5.post1-7-g4e234b7)
   c copyright: (C) 2012-2020 Massimo Lauria <massimo.lauria@uniroma1.it>
   c url: https://massimolauria.net/cnfgen
   c command line: cnfgen php 5 4
   c
   p cnf 20 45
   1 2 3 4 0
   5 6 7 8 0
   ...
   -16 -20 0
   
For a documentation on how to use ``cnfgen`` command please type
``cnfgen  --help``  and for  further  documentation  about a  specific
formula generator type ``cnfgen <generator_name> --help``.

Reference
---------
.. [1] http://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/satformat.ps
.. [2] http://www.latex-project.org/ 
.. [3] http://en.wikipedia.org/wiki/Proof_complexity

       
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


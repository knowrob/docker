
INSERT INTO Tutorial VALUES(5,'getting_started','Getting started','The user interface','The user interface consists of four panes with different purposes.

  * The *Prolog interaction pane* allows the user to type Prolog queries and commands and see the answers to these queries. Queries are to be typed in the lower area, the results will be shown in the box above.
  * A list of prepared queries with English translation is provided in the *query list pane* in the bottom left. If you click on an entry in this library, the corresponding Prolog query will be added to the query field.
  * The *3D display pane* in the upper right can visualize the robot and its environment in a 3D canvas. Other information such as trajectories, robot and object poses can also be added and highlighted.
  * The *visual analytics pane* in the lower right can visualize statistical data as bar charts and pie charts. Special query predicates allow to update the visualization panes with the results of queries.

**Note:** 
If the 3D display pane does not yet show a grid in the background, your knowledge
base has not yet been loaded completely. In this case, please wait a moment and
reload the page.',1);
INSERT INTO Tutorial VALUES(6,'getting_started','Getting started','Sending queries','The query language used in OpenEASE is Prolog, a logical programming language.
Queries consist of predicates that are linked by logical operators, usually the
AND operator (in Prolog represented by a comma '',''), or the OR operator
represented by a semicolon '';''. Queries need to be finished by a full stop ''.''
character. An example query has already been added to the query field:

    member(A, [a,b,c]).


The `member` predicate associates the variable A given as first argument (in
Prolog, variables start with an uppercase letter) to all elements of the list
that is given as second argument. In this example, the list consists of three
constants a, b, and c (constants start with a lowercase letter).
You can send the query with the key combination `CTRL + ENTER` (on Mac: `CMD +
ENTER`). Prolog will return the first result, the variable assignment

    A = a

If you would like to retrieve more results, you need to press `CRTL + ;`
(on Mac: `CMD + ;`), and Prolog will return the next solutions to your query:

    A = a 
    A = b 
    A = c 
    false

**Note:** In Prolog, the result `false` only means that no additional solutions
can be found. It does not mean that a query failed or that an error occurred.
The result `true`, on the other hand, only denotes that additional solutions
may exist, i.e. that the space of solutions has not yet been exhaustively searched.
',2);
INSERT INTO Tutorial VALUES(7,'getting_started','Getting started','Loading data','Experiment data may consist of different components -- semantic annotations
that are stored in OWL files, images that have been recorded during the task
which are stored as files on the disk, and position data that is stored in an
efficient high-volume database. The integration of these information sources
is transparent to the user, and all of them can be accessed via the same
Prolog query interface. 

You can load experiment data using the `load_experiment` predicate that parses
the OWL file with the high-level description, and does some housekeeping to
set up search paths for the other information sources.
In addition to the experiment data, you may want to load static background
knowledge such as a robot description or a semantic environment map. They
can be loaded using the `owl_parse(URL)` predicate that understands global
paths in the filesystem as well as URLs of the forms `http://...` and
`package://pkg-name/local/path/to/file`. The latter are a special kind of
URL used in the ROS ecosystem that reference files by their local path
w.r.t. a ROS package.',3);
INSERT INTO Tutorial VALUES(8,'getting_started','Getting started','Visualizing results','The query language has been extended by a set of special predicates that have
the side-effect of updating one of the visualization panels. They can simply
be appended to a query with a comma. Usually, they receive an object identifier,
a robot identifier or the identifier of a geometric frame plus the respective
time points as arguments. A complete list of the visualization predicates can
be found [here](http://knowrob.org/doc).

This marks the end of this short Tutorial. You can now go on, load some
experiment data, explore the queries we have prepared, and play around with them!
',4);

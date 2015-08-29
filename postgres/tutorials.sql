drop table if exists tutorial;
create table tutorial (
    id serial primary key,
    cat_id text not null,
    cat_title text not null,
    title text not null,
    text text not null,
    page integer not null
);

INSERT INTO Tutorial VALUES(0,'getting_started','Getting started','The user interface','The user interface consists of six panes with different purposes.

  * The *Prolog interaction area hl_console* in the upper left consists of the *history pane hl_history* in the top and the *query field hl_user&#95;query* at the bottom. Prolog queries are to be typed in the *query field hl_user&#95;query*, whereas the history of the queries with their respective results will be shown in the *history pane hl_history*.
  * The pane in which this tutorial text is now displayed, the *query list pane hl_library*, usually contains a list of prepared queries with English translation. If you click on an entry in this library, the corresponding Prolog query will be added to the *query field hl_user&#95;query*.
  * The *3D display pane hl_markers* in the upper middle can visualize the robot and its environment in a 3D canvas. Other information such as trajectories, robot and object poses can also be added and highlighted.
  * The *visual analytics pane hl_chart* in the lower middle can visualize statistical data as bar charts and pie charts. Special query predicates allow to update the visualization pane with the results of queries.
  * The *belief pane hl_designator* in  the upper right enables the user to inspect the internal data structures of the robot''s beliefs including object, action, and location descriptions used by the robot.
  * The *image pane hl_mjpeg* in the lower right is used for displaying images caputed by the robot''s camera.

All Panes except for the *3D display pane hl_markers* can be opened or closed by clicking the dark *grey bars hlc_ui-layout-toggler* on the edges or resized by dragging them.

**Note:** 
If the *3D display pane hl_markers* does not yet show a grid in the background, your knowledge
base has not yet been loaded completely. In this case, please wait a moment and
reload the page.',1);
INSERT INTO Tutorial VALUES(1,'getting_started','Getting started','Sending queries','The query language used in OpenEASE is Prolog, a logical programming language.
Queries consist of predicates that are linked by logical operators, usually the
AND operator (in Prolog represented by a comma '',''), or the OR operator
represented by a semicolon '';''. Queries need to be finished by a full stop ''.''
character. An example query has already been added to the query field:

    member(A, [a,b,c]).


The `member` predicate associates the variable A given as first argument (in
Prolog, variables start with an uppercase letter) to all elements of the list
that is given as second argument. In this example, the list consists of three
constants a, b, and c (constants start with a lowercase letter).
You can send the query with the *query button hl_btn&#95;query* or the key combination `CTRL + ENTER` (on Mac: `CMD +
ENTER`). Prolog will return the first result, the variable assignment

<pre>
A = a
</pre>
                            
If there are more solutions available, the *Next solutions button hl_btn&#95;query&#95;next* will be enabled. To retrieve more results, use this button or press `CRTL + n`
(on Mac: `CMD + n`), and Prolog will return the next solutions to your query:

<pre>
A = a 
A = b 
A = c 
false.
</pre>
                            
**Note:** In Prolog, the result `false` only means that no additional solutions
can be found. It does not mean that a query failed or that an error occurred.
The result `true`, on the other hand, only denotes that additional solutions
may exist, i.e. that the space of solutions has not yet been exhaustively searched.
',2);
INSERT INTO Tutorial VALUES(2,'getting_started','Getting started','Loading data','Experiment data may consist of different components -- semantic annotations
that are stored in OWL files, images that have been recorded during the task
which are stored as files on the disk, and position data that is stored in an
efficient high-volume database. The integration of these information sources
is transparent to the user, and all of them can be accessed via the same
Prolog query interface. 

You can load experiment data using the `load_experiments` predicate that parses
the OWL file with the high-level description, and does some housekeeping to
set up search paths for the other information sources.

    load_experiments(''/home/ros/knowrob_data/logs/robots/cram/'', [''pick-and-place'', ''dual-arm-pick-and-place'', ''tablesetting''], ''cram_log.owl'').

The example above loads the pick-and-place, dual-arm-pick-and-place and tablesetting experiments. 
In addition to the experiment data, you may want to load static background
knowledge such as a robot description or a semantic environment map. They
can be loaded using the `owl_parse(URL)` predicate that understands global
paths in the filesystem as well as URLs of the forms `http://...` and
`package://pkg-name/local/path/to/file`. The latter are a special kind of URL used in the ROS ecosystem that reference files by their local path
w.r.t. a ROS package.

    owl_parse(''package://knowrob_srdl/owl/PR2.owl'').
                            
Using the query above, you can load the model of the PR2 robot. This will not update the 3D visualization yet. The visualization of loaded data will be explained in the next step of this tutorial.',3);
INSERT INTO Tutorial VALUES(3,'getting_started','Getting started','Visualizing results','The query language has been extended by a set of special predicates that have
the side-effect of updating one or more of the visualization panels. They can simply
be appended to a query with a comma. Usually, they receive an object identifier,
a robot identifier or the identifier of a geometric frame plus the respective
time points as arguments. A complete list of the visualization predicates can
be found [here](http://knowrob.org/api/knowrob_vis).
                            
    owl_parse(''package://iai_semantic_maps/owl/room.owl''), add_object_with_children(''http://knowrob.org/kb/ias_semantic_map.owl#SemanticEnvironmentMap_PM580j'').
                            
The query above loads the semantic map and displays it in the *3D display pane hl_markers*.

',4);
INSERT INTO Tutorial VALUES(4,'getting_started','Getting started','Next steps','
After a successful [registration](https://data.open-ease.org/user/register) and login you are now able to run the different experiments provided by the AI research group by choosing one of the application from the dropdown menu. You can switch the experiments in the upper right of the openEASE menu bar. Now you can try out the example queries or use your own. 
                            
For more information about openEASE and the services it provides please have a look at the openEASE [introduction video](https://www.youtube.com/watch?v=iu_Y7mxDjgA) and the [overview paper](http://www.open-ease.org/wp-content/uploads/2015/03/knowrob-s.pdf).
                            
This marks the end of this introductory Tutorial. You can now go on, load some
experiment data, explore the queries we have prepared, and play around with them!
',5);

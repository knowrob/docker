drop table if exists tutorial;
create table tutorial (
    id serial primary key,
    cat_id text not null,
    cat_title text not null,
    title text not null,
    text text not null,
    page integer not null
);

INSERT INTO Tutorial VALUES(0,'getting_started','Getting started','The user interface',
'The user interface consists of six panes with different purposes.

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

INSERT INTO Tutorial VALUES(1,'getting_started','Getting started','Logic Programming (1)',
'The query language used in openEASE is [Prolog](http://www.swi-prolog.org), a logical programming language.
Queries consist of predicates that are linked by logical operators, usually the
AND operator (in Prolog represented by a comma '',''), or the OR operator
represented by a semicolon '';''. Queries need to be finished by a full stop ''.''
character. An example query is given below:

    member(A, [a,b,c]).


The `member` predicate associates the variable A given as first argument (in
Prolog, variables start with an uppercase letter and predicates start with a lower case letter)
to all elements of the list that is given as second argument.
In this example, the list consists of three
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
                    
**Note:** In Prolog, terms must stop with a fullstop (`.`) character.  

**Note:** In Prolog, the result `false` only means that no additional solutions
can be found. It does not mean that a query failed or that an error occurred.
The result `true`, on the other hand, only denotes that additional solutions
may exist, i.e. that the space of solutions has not yet been exhaustively searched.
',2);

INSERT INTO Tutorial VALUES(2,'getting_started','Getting started','Logic Programming (2)',
'A Prolog program consists of a number of clauses.
Each clause is either a fact or a rule.
After a Prolog program is consulted in a Prolog interpreter,
users can submit goals or queries,
and the Prolog intepreter will give results according to the facts and rules
in the knowledge base.

A fact must start with a predicate (which is an atom) and end with a fullstop.
The predicate may be followed by one or more arguments which are enclosed by parentheses.
The arguments can be atoms, numbers, variables or lists. Arguments are separated by commas.
For example, the fact `robot(''PR2'')` could denote the existence of a robot with the name ''PR2''.
Here, the predicate `robot` forms a *unary relation*.
Facts can be dynamically asserted into the knowledge base.

    assert(robot(''PR2'')),
    assert(robot(''BOXY'')),
    assert(robot(''JUSTIN'')).

These facts declare the existence of three robots with the names ''PR2'', ''BOXY'' and ''JUSTIN''.
In a Prolog program, a presence of a fact indicates a statement that is true. An absence of a fact indicates a statement that is not true. See the following example:

    robot(''PR2'').

Yields in
<pre>
true.
</pre>

    robot(''PR3'').

Yields in
<pre>
false.
</pre>

The arguments of facts can be supplied either bound (as in above examples) or unbound as variables.
In the latter case, Prolog tries to find bindings for the variable so that the statement
holds true. For example:

    robot(RobotUnbound).

Yields in:
<pre>
    RobotUnbound = ''PR3''
    RobotUnbound = ''BOXY''
    RobotUnbound = ''JUSTIN''
</pre>

Relations between entities can be expressed in a similar fashion.
For instance, this allows to span a component hierarchy.
First, we need facts that declare different components:

    assert(component(''Kinect'')),
    assert(component(''Gripper'')).

Based on the facts that we asserted in the knowledge base, we can define another predicate
that declares the component hierarchy:
    
    assert(has_component(''PR2'', ''Kinect'')),
    assert(has_component(''BOXY'', ''Kinect'')),
    assert(has_component(''PR2'', ''Gripper'')).

This allows, for instance, to query for all robots with a ''Kinect'' component:

    robot(Robot), has_component(Robot, ''Kinect'').

Yields in
<pre>
    Robot = ''PR2''
    Robot = ''BOXY''
</pre>

We can also easily query for robots with a ''Kinect'' component and a ''Gripper'' component available:

    robot(Robot), Components = [''Kinect'', ''Gripper''], forall( member(Component,  Components), has_component(Robot, Component) ).

Yields in
<pre>
    Robot = ''PR2''
</pre>

In above query, the predicate `forall` is used to successively bind one of the component names to the `Component` variable
in order to check if `has_component(Robot, Component)` holds true.
The call only yields *true* for robots with both components available.

This tutorial is only a brief introduction to logic programming with Prolog.
Please visit the [SWI Prolog](http://www.swi-prolog.org) website or one of the
many [Prolog tutorials](http://www.learnprolognow.org) available online.',3);

INSERT INTO Tutorial VALUES(3,'getting_started','Getting started','Web Ontology Language',
'Experiment data may consist of different components - semantic annotations
that are stored in the [Web Ontology Language](http://en.wikipedia.org/wiki/Web_Ontology_Language) (OWL),
images that have been recorded during the task
which are stored as files on the disk, and position data that is stored in an
efficient high-volume database. The integration of these information sources
is transparent to the user, and all of them can be accessed via the same
Prolog query interface.

In openEASE, all knowledge is represented in the Web Ontology Language.
This XML-based format allows to formally describe relational knowledge in a Description Logics (DL) dialect.
The OWL language is characterized by formal semantics and is built upon a W3C XML standard
for objects called the [Resource Description Framework](https://en.wikipedia.org/wiki/Resource_Description_Framework) (RDF).

The RDF data model is similar to classical conceptual modeling approaches such as entity-relationship or class diagrams,
as it is based upon the idea of making statements about resources (in particular web resources) in the form of subject-predicate-object expressions.
These expressions are known as triples in RDF terminology.
The subject denotes the resource, and the predicate denotes traits or aspects of the resource and expresses a relationship between the subject and the object. 
<pre>
&lt;owl:NamedIndividual rdf:about="http://knowrob.org/kb/PR2.owl#PR2Robot1"&gt;
    &lt;rdf:type rdf:resource="http://knowrob.org/kb/knowrob.owl#PR2"/&gt;
    &lt;srdl2-comp:succeedingLink rdf:resource="http://knowrob.org/kb/PR2.owl#pr2_base_footprint"/&gt;
    &lt;srdl2-comp:subComponent rdf:resource="&pr2;pr2_base"/&gt;
    ....
&lt;/owl:NamedIndividual&gt;
</pre>

Above OWL statement declares a subject with the name "http://knowrob.org/kb/PR2.owl#PR2Robot1".
`rdf:type` is a predicate that relates the robot with the corresponding type in the taxonomy.
Similarly, the relations `srdl2-comp:succeedingLink` and `srdl2-comp:subComponent` are used to span
a component hierarchy that describes which components belong to the PR2 robot.

In openEASE, you can load OWL files using the `owl_parse` predicate that parses
the OWL file with the high-level description.
The `owl_parse` predicate understands global
paths in the filesystem as well as URLs of the forms `http://...` and
`package://pkg-name/local/path/to/file`.
The latter are a special kind of URL used in the ROS ecosystem that reference files by their local path
w.r.t. a ROS package.

    owl_parse(''package://knowrob_srdl/owl/PR2.owl'').

This call asserts facts into the knowledge base based on the decalarations in the OWL file.
In this case, the OWL file contains knowledge about the model of the PR2 robot.

For formally modeling knowledge, it is very useful to distinguish between general relations and environment-specific information.
In OWL, this is reflected by the distinction between classes and instances.
Class knowledge is described in the so-called TBOX (terminological box);
knowledge about instances of these classes is contained in the ABOX (assertional box).
The relation between classes and instances is similar to object-oriented programming. 
An example TBOX query that queries for all parent classes of the class ''http://knowrob.org/kb/knowrob.owl#Robot'' is given below:

    owl_subclass_of(A, ''http://knowrob.org/kb/knowrob.owl#Robot'').

ABOX statements are about individuals of classes that are defined in the TBOX.
This includes, for example, to query for individuals of a given class:

    owl_individual_of(A, knowrob:''PR2'').

When OWL files are loaded into the system, they are internally stored as triples `rdf(Subject, Predicate, Object)`.
Using the predicate `rdf_has` we can query for the RDF triples that are declared in the OWL file.
This allows, for instance, to query for all sub-components of the PR2 robot.

    rdf_has(''http://knowrob.org/kb/PR2.owl#PR2Robot1'', ''http://knowrob.org/kb/srdl2-comp.owl#subComponent'', Components).

It is important to understand that KnowRob separates knowledge about the world
(which is, as far as possible, represented in OWL) from implementation issues and deduction rules
(which are implemented in plain Prolog).
OWL''s strict formal semantics, its typing and the existing reasoning methods are the main reasons for this separation.
In order to profit from these properties, it is thus necessary that information which is read from external sources
by Prolog predicates is transformed into a representation that is compatible to the OWL knowledge. 

**Note:** As usual, the predicate `rdf_has` supports an arbitrary number of arguments to be bound or unbound.

**Note:** For modeling with OWL, use the [Protege OWL editor](http://protege.stanford.edu/download/protege/4.1/installanywhere/) (version 4.x) which makes exploring and editing OWL files much easier and have a look at the documentation.
',4);

INSERT INTO Tutorial VALUES(4,'getting_started','Getting started','KnowRob Packages',
'If your application requires functionality beyond that one already provided by the standard KnowRob packages,
you will need to create your own KnowRob package.
The following description assumes that you would like to add knowledge in terms of OWL ontologies,
or implement new Prolog predicates, or both. If you would just like to link against Java libraries provided by KnowRob,
you don''t have to follow the description below, but can just implement a normal ROS package that depends on the respective KnowRob packages.

KnowRob packages are normal ROS packages that, in addition, contain some special files and folders.
This common structure allows tools like [rosprolog](http://www.ros.org/wiki/rosprolog) to automatically load the package and all its dependencies.
<pre>
  your_package
  |- package.xml
  |- CMakeLists.txt
  |- owl
  |  \\- your_file.owl
  |- prolog
     |- init.pl
     \\- your_module.pl
</pre>

The example above assumes that you would like to create a package `your_package` with an OWL ontology `your_file.owl`
and a Prolog file `your_module.pl`.
Consider wrapping your functionality into a Prolog module to increase modularity and to avoid name clashes.

The `init.pl` should initialize the package, which may include loading dependencies, parsing OWL files, and registering RDF namespaces.
When referring to OWL files, consider using URLs of the form `package://<pkg_name>/owl/file.owl` that reference files relative to a ROS package.
They are used by the [ROS resource_retriever](http://wiki.ros.org/resource_retriever) library and are also understood by the OWL parser in KnowRob.
You can have a look at e.g. `comp_spatial` for an example.
Once you have set up your package like this, you can register it in openEASE using:

    register_ros_package(your_package).


Like in any other ROS package, you will need to specify your dependencies in the `package.xml`.
Which packages to depend on depends on which functionality you would like to use.
You only need to list the direct dependencies, their dependencies are automatically included as well.
To use the minimal KnowRob functionality, you should depend on `knowrob_common` -
other common candidates are `knowrob_objects` for object/perception/spatial information-related things,
or `knowrob_actions` for representation and reasoning about actions.

In openEASE, you can define your own KnowRob packages with the experimental IDE in the "Editor" page.
When you are ready setting up your package, press the `Consult` menu entry in order to load
your packages.

**Note:** At the moment, it is not possible to compile code in user packages on openEASE. Thus, you can not include languages such as Java or C++ in your package.',5);

INSERT INTO Tutorial VALUES(5,'getting_started','Getting started','Marker Visualization',
'openEASE includes a browser-based visualization canvas that can display 3D data such as the environment map or the robot itself.
The canvas is based on [rosbridge](http://wiki.ros.org/rosbridge)
and the [robotwebtools](http://robotwebtools.org/) libraries that provide tools for displaying information from ROS in a browser.

For high compatibility with other ROS tools, openEASE uses the same visualization messages
that are used in the common ROS tool [rviz](http://wiki.ros.org/rviz).
In rviz, visual objects are described by, so called, [marker messages](http://wiki.ros.org/rviz/DisplayTypes/Marker).
Each message describes one visual object including the type of the object and the pose of the object.

The set of supported marker primitive types can be queried using the `marker_prop_type(Type,_)` predicate.
The primitive types include `arrow`, `cube`, `sphere`, `cylinder`, `line_strip`, `line_list`,
`cube_list`, `sphere_list`, `points`, `text_view_facing`, `mesh_resource` and `triangle_list`.
Primitive markers can be created using `marker($type(''Name''),_)`, where `$type` must be replaced by one of the primitive types.
Note that the term `$type(''Name'')` is the marker name that can be used to address this marker.

In addition to the primitive types, openEASE supports a set of complex marker types.

  * cylinder_tf(Frame0,Frame1): A cylinder between 2 links
  * link(Frame): A marker that takes the pose of a link
  * trajectory(Frame): A trajectory of a link
  * trail(Frame): A trail of a link (trajectory with alpha fade)
  * average_trajectory(Frame): The average over multiple trajectories
  * pointer(Frame0,Frame1): Arrow that points from Frame0 in the direction of Frame1
  * object(Name): A marker that represents an OWL individual (including children objects)
  * agent(Name): A marker that represents an OWL agent individual (including all links)
  * stickman(Name): A special human skeleton visualization, kinematic structure is spanned by the OWL individual indentified by Name

In openEASE, markers are automatically spawned in the canvas after they are asserted into the knowledge base
using the `marker` predicate.
Properties of markers, such as the pose, can be dynamically manipulated by calling predicates that
change the property value.

    marker(arrow(''A''),Arrow), marker_translation(Arrow, [0.0,0.0,0.0]), marker_scale(Arrow, [0.5,0.5,0.5]),
    marker(cube(''B''),Cube), marker_translation(Cube, [0.0,1.0,0.0]), marker_scale(Cube, [0.5,0.5,0.5]),
    marker(sphere(''C''),Sphere), marker_translation(Sphere, [0.0,2.0,0.0]), marker_scale(Sphere, [0.5,0.5,0.5]).

The second argument of the `marker` predicate is an object that holds the state of the marker.
Internally, this object is mapped to the marker name so that marker objects and marker names can be used
to identify a marker. For example, `marker_position(arrow(''A''), [0.0,0.0,0.0])` can also be used to
modify the position of the arrow marker.

openEASE supports the visualization of objects using 3D surface meshes in the STL or Collada file formats.
These meshes can either be attached to an object instance or to an object class,
in which case they are used for visualization of all of its instances.
The following OWL snippet shows how an instance can be linked to its CAD model using the `pathToCadModel` property: 

<pre>
&lt;owl:NamedIndividual rdf:about="&map_obj;milk1"&gt;
   &lt;rdf:type rdf:resource="&knowrob;CowsMilk-Product"/&gt;
   &lt;knowrob:pathToCadModel rdf:datatype="&xsd;string"&gt;
          package://knowrob_tutorial/cad/milk.kmz&lt;/knowrob:pathToCadModel&gt;
&lt;/owl:NamedIndividual&gt;
</pre>

As usual, the RDF triples can be queried using `rdf_has`

    rdf_has(Obj, knowrob:pathToCadModel, _).

Above queriy yields in all objects that have an associated CAD model.

Inside the ROS filesystem, resources such as binary files can be described using different kinds of URLs:
The common file:// and http:// URLs, and the package:// URL used above that describes a path relative to a ROS package.
These URLs can be resolved using the [resource_retriever](http://wiki.ros.org/resource_retriever) tool.

Since the client of a webserver cannot access the whole file system, this mechanism does not work as such if requests are made from a website.
The `ros3djs` library therefore rewrites package:// URLs for object meshes to subfolders of the website''s docroot.
For example, meshes in the package `pr2_description` are searched at `http://$IP/pr2_description/...`.

If you would like to reset the canvas to be empty, please use following call:

    marker_remove(all).

**Note:** Remove individual markers with `marker_remove` by binding a marker name to the predicate argument.',6);

INSERT INTO Tutorial VALUES(6,'getting_started','Getting started','Next steps','
After a successful [registration](https://data.open-ease.org/user/register) and
login you are now able to run the different experiments provided by the AI research group by choosing one of the application from the dropdown menu.
You can switch the experiments in the upper right of the openEASE menu bar.
Now you can try out the example queries or use your own. 
                            
For more information about openEASE and the services it provides please have a look at
the openEASE [introduction video](https://www.youtube.com/watch?v=iu_Y7mxDjgA)
and the [overview paper](http://www.open-ease.org/wp-content/uploads/2015/03/knowrob-s.pdf).
                            
This marks the end of this introductory Tutorial. You can now go on, load some
experiment data, explore the queries we have prepared, and play around with them!
You can also continue with in depth tutorials by clicking on the *next* button below.
The remaining tutorials cover different aspects of the knowledge processing service openEASE
including the representation of semantic maps, tasks and actions, objects and locations
as well as representation of kinematic chains and robot capabilities.
',7);

/*INSERT INTO Tutorial VALUES(2,'getting_started','Getting started','Loading data','Experiment data may consist of different components -- semantic annotations
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
*/

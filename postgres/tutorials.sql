drop table if exists tutorial;
create table tutorial (
    id serial primary key,
    cat_id text not null,
    cat_title text not null,
    title text not null,
    text text not null,
    page integer not null
);

INSERT INTO Tutorial VALUES(110,'overview','openEASE Tutorials','Tutorial List',
'
  * <a class="tut_cat_link" onclick="loadTutorial(''getting_started'',1)">Getting started</a>
  * <a class="tut_cat_link" onclick="loadTutorial(''map'',1)">Semantic map</a>
  * <a class="tut_cat_link" onclick="loadTutorial(''actions'',1)">Actions and tasks</a>
  * <a class="tut_cat_link" onclick="loadTutorial(''objects'',1)">Objects and locations</a>
  * <a class="tut_cat_link" onclick="loadTutorial(''srdl'',1)">Semantic robot description</a>
',1);

/*****************************************************************************************/
/*****************************************************************************************/
/*****************************************************************************************/
/*****************************************************************************************/

INSERT INTO Tutorial VALUES(220,'getting_started','Getting started','The user interface',
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

INSERT INTO Tutorial VALUES(221,'getting_started','Getting started','Logic Programming (1)',
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

INSERT INTO Tutorial VALUES(222,'getting_started','Getting started','Logic Programming (2)',
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
    RobotUnbound = PR2
    RobotUnbound = BOXY
    RobotUnbound = JUSTIN
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
    Robot = PR2
    Robot = BOXY
</pre>

We can also easily query for robots with a ''Kinect'' component and a ''Gripper'' component available:

    robot(Robot), Components = [''Kinect'', ''Gripper''], forall( member(_Component,  Components), has_component(Robot, _Component) ).

Yields in
<pre>
    Robot = PR2
</pre>

In above query, the predicate `forall` is used to successively bind one of the component names to the `_Component` variable
in order to check if `has_component(Robot, _Component)` holds true.
The call only yields *true* for robots with both components available.
Note that variable that start with an underscore are not returned as result.

This tutorial is only a brief introduction to logic programming with Prolog.
Please visit the [SWI Prolog](http://www.swi-prolog.org) website or one of the
many [Prolog tutorials](http://www.learnprolognow.org) available online.',3);

INSERT INTO Tutorial VALUES(223,'getting_started','Getting started','Web Ontology Language',
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

**TODO** namespaces

**Note:** As usual, the predicate `rdf_has` supports an arbitrary number of arguments to be bound or unbound.

**Note:** For modeling with OWL, use the [Protege OWL editor](http://protege.stanford.edu/download/protege/4.1/installanywhere/) (version 4.x) which makes exploring and editing OWL files much easier and have a look at the documentation.
',4);

INSERT INTO Tutorial VALUES(224,'getting_started','Getting started','KnowRob Packages',
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

INSERT INTO Tutorial VALUES(225,'getting_started','Getting started','Marker Visualization',
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

    marker(arrow(''A''),Arrow), marker_translation(Arrow, [0.0,0.0,0.0]), marker_scale(Arrow, [1.0,0.4,0.4]).,
    marker(cube(''B''),Cube), marker_translation(Cube, [0.0,1.0,0.0]), marker_scale(Cube, [0.5,0.5,0.5]),
    marker(sphere(''C''),Sphere), marker_translation(Sphere, [0.0,2.0,0.0]), marker_scale(Sphere, [0.5,0.5,0.5]).

The second argument of the `marker` predicate is an object that holds the state of the marker.
Internally, this object is mapped to the marker name so that marker objects and marker names can be used
to identify a marker. For example following query can also be used to modify the position of the arrow marker:

    marker_translation(arrow(''A''), [0.0,1.0,0.0]).

Marker properties can be modified dynamically, for instance, in order to change the color os a marker:

    marker_color(arrow(''A''), [0.4,0.4,0.9]).

Additionally, markers can be highlighted using the `marker_highlight` predicate:

    marker_highlight(arrow(''A'')).

And the highlight can be removed again by calling:

    marker_highlight_remove(arrow(''A'')).

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

**Note:** To get an full overview about the marker API, please take a look at the [github project page](https://github.com/knowrob/knowrob/tree/master/knowrob_vis).

**Note:** Remove individual markers with `marker_remove` by binding a marker name to the predicate argument.',6);

INSERT INTO Tutorial VALUES(226,'getting_started','Getting started','Next steps','
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

/*****************************************************************************************/
/*****************************************************************************************/
/*****************************************************************************************/
/*****************************************************************************************/

INSERT INTO Tutorial VALUES(330,'map','Semantic map','Semantic Map Representation',
'Semantic maps are descriptions of an environment in terms of localized object instances and are stored in OWL files. Much of the environment- and object-related functionality in KnowRob depends of having a valid semantic map, so you may want to create one for your robot''s environment.

<img src="http://knowrob.org/_media/part-of-hierarchy-map.png" alt="Smiley face" height="168" width="320">

There are different ways how to create a semantic map in OWL:

  * Semantic Map Editor: The Semantic Map Editor is a graphical editor for semantic maps. It can be used to create object instances and to set their positions. The current version is rather specific for indoor environments though and, for example, offers only a limited set of object types to be added to the map. You can easily adapt the list of classes in the source code, but this cannot conveniently be configured at the moment.
  * SemanticMapToOWL: If you already have a map datastructure and would like to create a semantic map from your program, the SemanticMapToOWL ROS service is probably the easiest solution. It accepts a SemanticMap message and returns the OWL data as a string.
  * Robot perception system: If you have integrated a perception system with KnowRob, a kind of semantic map is automatically created by the objects the robot perceives. You can save the in-memory map to an OWL file using the methods in the owl_export module.
  * Manual creation of the OWL file: In some cases, it may actually be the fastest to create the map manually in a good text editor in which you can copy and paste the object instances and their pose matrices. Especially if you would like to set many semantic object properties beyond their poses, this may be a good option. If you plan to do this, you should have well understood how object poses are represented in KnowRob.

Loading a semantic map:
 
    owl_parse(''package://iai_semantic_maps/owl/kitchen.owl'').

Visualization of the loaded map:
 
    marker_update(object(''http://knowrob.org/kb/IAI-kitchen.owl#IAIKitchenMap_PM580j'')).
',1);

INSERT INTO Tutorial VALUES(331,'map','Semantic map','Reasoning about Articulated Objects',
'Articulated objects, e.g. cupboards, that have doors or drawers are represented in a special way to describe, on the one hand, the component hierarchy, and, on the other hand, which connections are fixed and which are movable. Like for other composed objects, there is a part-of hierarchy (properPhysicalParts). Joints are parts of the cupboard/parent object, and are fixed-to (connectedTo-Rigidly) both the parent and the child (e.g. the door). In addition, the child is hingedTo or prismaticallyConnectedTo the parent.

Joints are described using the following properties, which are compatible to the representation used by the ROS articulation stack:

  * Type: At the moment, rotational and prismatic joints are supported (knowrob:''Hinge'' and knowrob:''PrismaticJoint'')
  * Parent, Child: resp. object instances
  * Pose: like for normal objects using e.g. a SemanticMapPerception instance
  * Direction: vector giving the opening direction of a prismatic joint
  * Radius: radius of a rotational joint (e.g. between handle and hinge)
  * Qmin, Qmax: lower and upper joint limits

Reading Articulation Information:

There are some helper predicates for reading, creating, updating and deleting joints from articulated objects. This task is on the one hand rather common, on the other hand somewhat complex because the structure visualized in the previous image needs to be established. To create a joint of type knowrob:''HingedJoint'' between two object parts at position (1,1,1) with unit orientation, radius 0.33m and joint limits 0.1 and 0.5 respectively, one can use the following statement: 

    create_joint_information(knowrob:''HingedJoint'', 
    iai_maps:''iai_kitchen_sink_area_left_middle_drawer_handle'', 
    iai_maps:''iai_kitchen_sink_area_left_bottom_drawer_main'', 
    [1,0,0,1,0,1,0,1,0,0,1,1,0,0,0,1], [], ''0.33'', ''0.1'', ''0.5'', Joint).


If a prismatic joint is to be created instead, the empty list [] needs to be replaced with a unit vector describing the joint''s direction, e.g. [0,0,1] for a joint opening in z-direction, and the joint type needs to be set as ''PrismaticJoint''. Joint information can conveniently be read using the following predicate that requires a joint instance as argument:

    read_joint_information(Joint, Type, Parent, Child, Pose, Direction, Radius, Qmin, Qmax).


To update joint information, one can use the following predicate:

    update_joint_information(Joint, knowrob:''HingedJoint'', [1,0,0,2,0,1,0,2,0,0,1,2,0,0,0,1], [1,2,3], 0.32, 1.2, 1.74).
',2);

INSERT INTO Tutorial VALUES(332,'map','Semantic map','Inferring likely storage locations',
'For some tasks, robots need to reason about the nominal locations of objects, for example when cleaning up or when unpacking a shopping basket. There are different techniques for inferring the location where an object should be placed:

  * Using assertions of the storagePlaceFor property is a rather generic, though not very adaptive technique that allows to state e.g. that perishable items belong into the refrigerator. It does not require any knowledge about the environment, but since it works on the level of object classes, it cannot choose between containers of the same type, e.g. different cupboards.

  * A finer-grained solution is based on organizational principles that places objects at the location where semantically similar objects are stored. It requires some (partial) knowledge about the distribution of other objects in the environment.

Querying for likely storage locations:

The simple option based on the storagePlaceFor predicate can be queried as follows in order to determine where an object (instance or class) shall be stored, or which known objects are to be stored in a given container

    owl_subclass_of(T, knowrob:''StorageConstruct''), class_properties(T, knowrob:''typePrimaryFunction-StoragePlaceFor'', knowrob:''Perishable''), owl_individual_of(Obj, T), marker_highlight(object(Obj)).
',3);

/*****************************************************************************************/
/*****************************************************************************************/
/*****************************************************************************************/
/*****************************************************************************************/

INSERT INTO Tutorial VALUES(440,'actions','Actions and Tasks','Action representation (1)','
In openEASE, instances of actions are represented in the ABOX of the OWL reasoner.
These action instances may be

  * actually observed or performed actions (something that happened at a certain time)
  * planned actions (something one intends to do)
  * inferred actions (something one imagines that happens)
  * asserted actions (some action someone told me has happened)

In any case, one talks about an action that could be asserted a (past or future) time and actor.

In contrast, the TBOX describes general information about classes of actions.
These can be quite general classes like `PuttingSomethingSomewhere`,
or very specific ones like `PuttingDinnerPlateInCenterOfPlacemat`.
However, all these class specifications describe types of actions that,
when they are actually executed, get instantiated to the corresponding actions in the ABOX.
Following query yields in all action classes defined in the core ontology:

    owl_subclass_of(A, knowrob:''Action'').

',1);

INSERT INTO Tutorial VALUES(441,'actions','Actions and Tasks','Action representation (2)','
Episodic memory can be loaded using the `load_experiments` predicate that parses
the OWL file with the high-level description, and does some housekeeping to
set up search paths for the other information sources.

    load_experiment(''/episodes/Pick-and-Place/xsens-kitchen-pnp_0/episode1/log.owl'').

As an example, let''s have a look at an instance of the class
`PuttingSomethingSomewhere` that corresponds to transporting an object from one position to another.
Obviously, this kind of action involves to pick up the object, move to the goal position,
and put the object down again. These sub-events are modeled in the following piece of OWL code: 

<pre>
&lt;owl:NamedIndividual rdf:about="&knowrob;PuttingSomethingSomewhere_KKxZYXiM"&gt;
    &lt;rdf:type rdf:resource="&knowrob;PuttingSomethingSomewhere"/&gt;
    &lt;knowrob:startTime rdf:resource="&knowrob;timepoint_1398864734.5133333"/&gt;
    &lt;knowrob:endTime rdf:resource="&knowrob;timepoint_1398864735.8466668"/&gt;
    &lt;knowrob:objectActedOn  rdf:resource="&knowrob;Cup_dsf784635"/&gt;
    &lt;knowrob:toLocation rdf:resource="&knowrob;drawer_island_left_lower"/&gt;
&lt;/owl:NamedIndividual&gt;
</pre>

The RDF triples can be accessed using the `rdf_has` predicate:

    owl_individual_of(Task, knowrob:''PuttingSomethingSomewhere''),
    rdf_has(Task, knowrob:''objectActedOn'', Obj),
    rdf_has(Task, knowrob:''toLocation'', Loc).

Complex robot tasks can be decomposed into primitive actions and movements.
If the sub-actions for lower-level actions are already modeled,
tasks can be described conveniently on a rather abstract level,
like the already mentioned `PuttingSomethingSomewhere` actions
which has no sub-actions but may has successor and predecessor actions:

    owl_individual_of(Task, knowrob:''PuttingSomethingSomewhere''),
    rdf_has(Task, knowrob:''nextEvent'', Next),
    rdf_has(Task, knowrob:''previousEvent'', Prev).

',2);

INSERT INTO Tutorial VALUES(442,'actions','Actions and Tasks','Action requirements','
Actions can have prerequisites in terms of components or capabilities
a robot needs to have in order to execute them.
The Semantic Robot Description Language (SRDL) allows to describe robot components,
robot capabilities, and dependencies of actions.

The following are just some examples, a full overview of SRDL can be found later in the tutorial. 

    required_cap_for_action(knowrob:''PuttingSomethingSomewhere'', Cap).

After loading a robot definition, the action requirements
can be matched against the available capabilities to determine which ones are missing:

    owl_parse(''package://knowrob_srdl/owl/PR2.owl''),
    missing_cap_for_action(knowrob:''PuttingSomethingSomewhere'', pr2:''PR2Robot1'', M).
',3);

/*
INSERT INTO Tutorial VALUES(443,'episodes','Episodic memory','Robot action logs','
openEASE provides a set of predicates for querying action logs.
First, let''s load an episode of a robot performing a pick and place task:

    load_experiment(''/episodes/Safe-Interaction/hospital-pick-and-place_0/episode1/cram_log.owl'').

    task(T),
    findall(_SubTask, subtask(T, _SubTask), SubTasks),
    not(SubTasks =  []).

    task_type(T,knowrob:''GraspingSomething''),
    task_start(T, Start),
    task_end(T, Start).
',4);
*/

/*
INSERT INTO Tutorial VALUES(444,'episodes','Episodic memory','Robot action logs','
Combining Semantic Map entities with action logs

    task(T),
    rdf_has(T, knowrob:''goalLocation'', LocationDesignator),
    rdf_has(map:''Fridge_87fguihg'', knowrob:''equatedDesignator'', LocationDesignator).
',4);
*/

/*
INSERT INTO Tutorial VALUES(555,'objects','Objects and locations','Pattern language',
'
*TODO* Pattern language
',6);
*/

INSERT INTO Tutorial VALUES(445,'actions','Actions and Tasks','Action statistics','
The comprehensive robot action logs of manipulation task episodes allows to
statistically investigate the plan execution.
openEASE offers a set of different diagram types for this purpose
which are introduced in this tutorial page.

Let''s first load the action of a robot performing amnioulation tasks:

    load_experiment(''/episodes/Pick-and-Place/pr2-general-pick-and-place_0/episode1/log.owl'').

Failure recovery is an important aspect of plan executioners.
It requires the detection of failures during runtime based on
sensory data.
In openEASE, action logs usually contain information about the
success of an action.
This is valuable information that can help to identify problematic actions
and to investigate why the action failed.
Failures are represented as instances of failure classes.
In most episodes on openEASE, the base class of action failures
is `CRAMFailure`.
Following code shows all logged failures in a pie chart:

    findall(Type-Num, (
        owl_subclass_of(T, knowrob:''CRAMFailure''),
        rdf_split_url(_, Type, T),
        findall(F, failure_type(F, T), Failures),
        length(Failures, Num)
    ), Distrib),
    pairs_keys_values(Distrib, Types, Nums),
    add_diagram(errordist, ''Error distribution'', piechart, xlabel, ylabel, 350, 350, ''11px'', [[Types, Nums]]).

In this query, all failure instances of a given failure class are queried using the `failure_type` predicate.
The name of the failure type and the number of instances are then used to parametrize the pie chart
which is send to the browser client using the predicate `add_diagram`.

Following query can be used to generate a timeline over all performed
actions in an episode:

    findall(_Y-(_T0-_T1), (
        rdfs_instance_of(_X, knowrob:''PurposefulAction''),
        event_class_name(_X,_Y),
        event_interval(_X,_T0,_T1)
    ), _Actions),
    pairs_keys_values(_Actions, ClassNames, _Times),
    pairs_keys_values(_Times, StartTimes, EndTimes),
    add_timeline(''actions'', ''Logged Actions'', ClassNames, StartTimes, EndTimes).

First, `rdfs_instance_of` is used to bind a `PurposefulAction` and the predicate
`event_interval` is used in order to query the start and end time of that action.
All matching actions are collected by the Prolog backtracker and saved into
the list `_Actions`. The event names and intervals are then used as arguments
for the call of the predicate `add_timeline` which causes the server to send
a diagram message to the browser client.

',4);

/*****************************************************************************************/
/*****************************************************************************************/
/*****************************************************************************************/
/*****************************************************************************************/

INSERT INTO Tutorial VALUES(550,'objects','Objects and locations','Visualize objects',
'We have separated the semantic environment map and the set of (smaller) objects inside the environment,
such as objects inside the cupboards and drawers.
This is commonly a good practice since it allows to use the same (often mostly static) map in different settings.
In real tasks, the set of objects is usually detected by the robot during operation and updated over time,
but for testing purposes, we load some objects from a file. 

    owl_parse(''package://knowrob_map_data/owl/ccrl2_semantic_map.owl''),
    owl_parse(''package://knowrob_basics_tutorial/owl/ccrl2_map_objects.owl'').
    
Once the map and the example objects have been loaded,
you can add the objects to the 3D canvas.
If definitions for CAD models of objects are loaded, these models are automatically used for visualizing object instances.
Otherwise, the system uses grey boxes as default visualization models.

    marker_update(object(''http://knowrob.org/kb/ias_semantic_map.owl#SemanticEnvironmentMap0'')).

Similarly, we can also visualize small objects in the kitchen:

    findall(A, ((
        owl_individual_of(A, knowrob:''FoodUtensil'');
        owl_individual_of(A, knowrob:''FoodVessel'');
        owl_individual_of(A, knowrob:''FoodOrDrink'')
    )), Objs),
    member(Obj,Objs),
    marker_update(object(Obj)).

Composed objects and their parts are linked by a ''parts'' hierarchy,
described using the `properPhysicalParts` property in OWL.
This property is transitive, i.e. a part of a part of an object is also a part of the object itself.
You can read all parts and sub-parts of an object using `owl_has`,
which takes the transitivity into account.
In the example below, `Handle160` is a part of `Door70`, which by itself is part of `Refrigerator67`. 

    owl_has(knowrob:''Refrigerator67'', knowrob:properPhysicalParts, P).
',1);

INSERT INTO Tutorial VALUES(551,'objects','Objects and locations','Query for objects',
'Since all objects in the map are instances of the respective object classes,
one can query for objects that have certain properties or belong to a certain class.

For example, a query for perishable objects can be written as:

    owl_individual_of(A, knowrob:''Perishable'').

Instances of the class `HandTool` (e.g. silverware) can be grasped by the robot:

    owl_individual_of(A, knowrob:''HandTool'').

In the kitchen domain, instances of the class `FoodVessel` (i.e. pieces of tableware)
might be important for the plan execution:

    owl_individual_of(A, knowrob:''FoodVessel'').

When grasping an object, the robot has to compute a grasping point on the object.
In openEASE, we decompose objects into functional parts so that we can reason 
about object parts. This allows, for example, to compute a grasping point
on the handle part of an object.
A query for all objects with handles can be written as:

    owl_has(A, knowrob:properPhysicalParts, H),
    owl_individual_of(H, knowrob:''Handle'').
',2);

INSERT INTO Tutorial VALUES(552,'objects','Objects and locations','Qualitative spatial relations',
'Qualitative spatial relations between objects can be computed using computable relations.

For example, the computable raltion `in-ContGeneric` checks wether the contains relation holds
for an object and a container.
This allows, for instance, to find the container that contains the object `cheese1`:

    rdf_triple(knowrob:''in-ContGeneric'', ''http://knowrob.org/kb/ccrl2_map_objects.owl#cheese1'', C).

Furthermore, it can be used to query for all object that are located in a given container:

    rdf_triple(knowrob:''in-ContGeneric'', O, knowrob:''Refrigerator67'').

Another computable relation is the `on-Physical` relation that checks
if an object is on top of another object:

    rdf_triple(knowrob:''on-Physical'', A, knowrob:''Dishwasher37'').
',3);

INSERT INTO Tutorial VALUES(553,'objects','Objects and locations','Object poses',
'Object poses are represented as instances of the class `SemanticMapPerception`
which is a subclass of `Event` and thus has properties that define the 
time interval of the event.
The event is related to the object using the `objectActedOn` property.
It is intended, that there can be multiple `SemanticMapPerception` events
for the same object in order to represent pose changes over time.

The OWL individual that represents the `SemanticMapPerception` can be written as:

<pre>
&lt;owl:NamedIndividual rdf:about="&map_obj;SemanticMapPerception138"&gt;
    &lt;rdf:type rdf:resource="&knowrob;SemanticMapPerception"/&gt;
    &lt;knowrob:startTime rdf:resource="&map_obj;timepoint_1336487125"/&gt;
    &lt;knowrob:eventOccursAt rdf:resource="&map_obj;RotationMatrix3D137"/&gt;
    &lt;knowrob:objectActedOn rdf:resource="&map_obj;cup1"/&gt;
&lt;/owl:NamedIndividual&gt;
</pre>

The actual pose of the object is represented in the `RotationMatrix3D137` instance
that contains a 4x4 transformation matrix.
In order to look up all object poses associated to an object of interest,
use the `rdf_has` predicate.

    rdf_has(Event, knowrob:objectActedOn, ''http://knowrob.org/kb/ccrl2_map_objects.owl#cheese1''),
    owl_individual_of(Event, knowrob;''SemanticMapPerception'').

In most cases, we are interested in the latest object pose while ignoring earlier pose estimates.
For convinience, openEASE offers the predicate `current_object_pose` in order to query
the latest perceived object pose.

    current_object_pose(''http://knowrob.org/kb/ccrl2_map_objects.owl#cheese1'', Pose).
',4);

INSERT INTO Tutorial VALUES(554,'objects','Objects and locations','Object locations',
'Commonsense knowledge about typical object locations was acquired by the
[Open Mind Indoor Common Sense](http://openmind.hri-us.com/) (OMICS) project.
We processed the natural language database entries and translated them to well-defined concepts
within the openEASE ontology as described in
[Putting People''s Common Sense into Knowledge Bases of Household Robots](http://ias.cs.tum.edu/_media/spezial/bib/kunze10omics.pdf).

You have to register the `knowrob_omics` package first:

    register_ros_package(knowrob_omics).

To query the probability of finding an object in a given room type you can use the following query:

    probability_given(knowrob:''OmicsLocations'', Obj, knowrob:''Kitchen'', Pr).

If you are interested in what type of room you could find a given object use the following query: 

    bayes_probability_given(knowrob:''OmicsLocations'', Room, knowrob:''Sandwich'',Pr).
',5);

/*
INSERT INTO Tutorial VALUES(555,'objects','Objects and locations','Visualize objects',
'
*TODO* Designator/Perception integration
  - dough size during pizza rolling
',6);
*/

/*****************************************************************************************/
/*****************************************************************************************/
/*****************************************************************************************/
/*****************************************************************************************/

INSERT INTO Tutorial VALUES(660,'srdl','Semantic robot description','Introduction',
'Inside KnowRob Framework, we also represent symbolic descriptions of robot components and capabilities. Such a knowledge can help us find out if a certain robot has all prerequisites for executing an action. The semantic descriptions of robots are defined using the Semantic Robot Description Language (SRDL). 

In order to start capability reasonig. First we need to register the ros package which loads SRDL into our Prolog session:

    register_ros_package(''knowrob_srdl'').
',1);

INSERT INTO Tutorial VALUES(661,'srdl','Semantic robot description','Kinematic Robot Model',
'The Semantic Robot Description Language (SRDL) is a logical language for describing robot hardware, software and capabilities. More information on the usage of SRDL for modeling a robot, for answering queries about its hardware configuration and for checking requirements of actions on robot components. Several SRDL models for popular robots (e.g. PR2, Baxter, TUM-Rosie, Amigo) are already contained in the mod_srdl package in the KnowRob stack. In order to facilitate the creation of an SRDL model for a new robot, there is a converter by A. Perzylo and P. Freyer that can read an URDF robot model and convert the kinematic structure to SRDL (www.knowrob.org). 

For this exercise, we can load the SRDLs of PR2 and Baxter:

    owl_parse(''package://knowrob_srdl/owl/PR2.owl''), owl_parse(''package://knowrob_srdl/owl/baxter.owl'').
',2);

INSERT INTO Tutorial VALUES(662,'srdl','Semantic robot description','Components of a robot',
'Read all components of a robot. There is no distinction between robots and components any more, robots are just complex components that consist of many parts.

    sub_component(pr2:''PR2Robot1'', Sub).


Filter the list of components to only those of a given type, e.g. a Camera:

    sub_component(pr2:''PR2Robot1'', Sub),  owl_individual_of(Sub, srdl2comp:''Camera'').


Check whether a component of a certain type exists on a robot (or, in general, as part of another component):

    comp_type_available(pr2:''PR2Robot1'', srdl2comp:''Camera'').
',3);

INSERT INTO Tutorial VALUES(663,'srdl','Semantic robot description','Capabilities of a robot',
'Add an action to our Prolog session so that we can reason about which capabilities are needed for it:

    register_ros_package(knowrob_actions), owl_parse(''package://knowrob_actions/owl/serve_drink.owl'').


Check which capabilities exists on a robot:

    cap_available_on_robot(Cap, pr2:''PR2Robot1'').



Capabilities an action depends on:

    required_cap_for_action(serve_drink:''ServeADrink'', C).


Missing capability of the given robot for an action:

    missing_cap_for_action(serve_drink:''ServeADrink'', baxter:baxter_baxter1, C).
',4);


/*****************************************************************************************/
/*****************************************************************************************/
/*****************************************************************************************/
/*****************************************************************************************/

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

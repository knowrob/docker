
/***********************************
 * Dependencies
 */
:- register_ros_package(knowrob_common).
:- register_ros_package(knowrob_srdl).
:- register_ros_package(knowrob_cram).

/***********************************
 * Include source files
 */
:- use_module(library('test')).

/***********************************
 * Parse OWL files
 */
:- owl_parser:owl_parse('package://%(pkgName)s/owl/test.owl').

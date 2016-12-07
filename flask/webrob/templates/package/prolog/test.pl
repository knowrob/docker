
:- module(test,
    [
      eats/2
    ]).
:- use_module(library('semweb/rdf_db')).
:- use_module(library('semweb/rdfs')).
:- use_module(library('owl')).
:- use_module(library('jpl')).
:- use_module(library('rdfs_computable')).
:- use_module(library('owl_parser')).
:- use_module(library('comp_temporal')).

eats(fred,foo). /* "Fred eats oranges" */

eats(fred,t_bone_steaks). /* "Fred eats T-bone steaks" */

eats(tony,apples). /* "Tony eats apples" */

eats(john,apples). /* "John eats apples" */

eats(john,grapefruit). /* "John eats grapefruit" */


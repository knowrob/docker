
:- module(test,
    [
      eats/2
    ]).

eats(fred,foo). /* "Fred eats oranges" */

eats(fred,t_bone_steaks). /* "Fred eats T-bone steaks" */

eats(tony,apples). /* "Tony eats apples" */

eats(john,apples). /* "John eats apples" */

eats(john,grapefruit). /* "John eats grapefruit" */

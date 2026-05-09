# Tactics for coloring treemaps

The first version of the treemap project, introduced in Fall 2024, 
randomly assigned contrasting (tile, text) color pairs at group or 
tile level.   Typically I would run a treemap a few times on the 
same data until I obtained a color scheme that was not _too_ 
terrible.  In summer 2025 I am attempting to replace random color 
choice by (optional, at least) user-specified color schemes.  

## Why did the first version have such a sucky approach to colors? 

In software development, we must often _design to schedule_, 
creating an initial version of a system on a schedule that is 
insufficient for producing all the features we envision in the form 
we would prefer.  There are several reasons to prefer an initial, 
limited version of software within a constrained schedule to a 
more complete, better system on a longer schedule.  Sometimes 
deadlines follow some external events.  For example, in the U.S. a 
game development team may need to deliver a shippable product by 
September to hit the crucial holiday shopping season.  For the 
treemap project, the beginning of fall 
term classes at University of Oregon was a key deadline for 
producing a usable project with adequate documentation. 

Even when  no external event drives a deadline, there are many 
reasons to prefer producing a limited product early to producing a 
better product later.  In a commercial or industrial project, 
shipping early can be essential to building customer interest or 
maintaining client commitment.  In addition, experience with an 
initial version, including customer or client feedback, informs and 
improves subsequent versions, even to the extent sometimes of 
informing a complete "pivot" to exploit unforeseen opportunities. 
For the treemap project, it was important to assess whether 
treemapping was a suitable project for the end of CS 210 at 
University of Oregon, and worth investment of more development time 
to share with instructors at other institutions.

## Preparing for change 

It was clear from the outset of project development in Spring 2024 
that random choice of colors was not a very good tactic.  It 
followed a common design technique in agile software development: 
Start with the simplest thing that could possibly work.  

There are certain constraints on _the simplest thing that could 
possibly work_.   For an internal prototyping step, it may be enough 
that the _stub_ solution not block development of other parts of a 
software system.  For a _minimum viable product_ provided to users, 
to _work_ must mean that the product is still somewhat usable in the 
initial version.  It won't be _as good_ as the envisioned system, 
but it needs to be (even just barely) _adequate_ to a product that 
is somewhat useful.  

In addition, there should be a _path forward_ from an initial 
version to better versions.  This is largely a constraint on 
modularity of the initial software system.  The first principle of 
modular design is isolating, to the degree feasible, anticipated 
software changes.   Initial stub versions of a feature are ipso 
facto anticipated future changes, so some thought must be given to 
localizing those changes.   In the treemap project, this meant that 
that _mapper_ component developed by students should delegate color 
decisions to the _display_ module provided by the instructor. 

## Design desiderata for user-controlled color schemes

Version 0 (summer 2024 for fall term 24) was designed to these criteria:

- Color assignments are isolated in the `display` module, which 
  students do not have to modify.  Replacing the color assignment 
  tactic should not require modifications to the `mapper` module 
  constructed by students.
- Colors in the Tk display are the same as colors in the SVG output. 
  This was an "at least minimally usable" requirement.
- Color pairs (tile, text label) adequately contrast as defined by 
  WCAG criteria.  This is partly a usability requirement and partly 
  an attempt to model responsible software development practices. 

For version 1 (summer 2025) my design goals include those above, and 
in addition

- For SVG output, a user-provided CSS stylesheet should take 
  precedence.  The CSS should be as simple and predictable as 
  possible.
  - Non-requirement:  Tk display may not follow CSS style sheet.  
    This is a practical decision to avoid trying to interpret a 
    potentially complex CSS stylesheet. 
- If a color scheme is provided in the form of a CSV table, it will 
  govern colors in the Tk display.  If there is _no_ CSS 
  style sheet, the Tk color display will also apply to the SVG output. 
- If neither CSS (for SVG) nor CSV (for Tk) is provided, colors will 
  be chosen in some arbitrary manner  (maybe random, or maybe a 
  default uniform color scheme like black text on white tiles).

The greater flexibility of creating a color scheme raises the issue 
of what to do with tiles whose color is not specified, either 
intentionally or due to a mistake (e.g., a misspelling) in the color 
specification.  This should be predictable, useful for creating 
simple specifications for complex schemes (e.g., "all the natural
science majors are light blue, except the pre-med majors are darker
blue").   To this end, our tentative design is: 

- If a tile without a specified color belongs to a group with a 
  specified color, it will inherit the color of the closest 
  enclosing group with a defined color. 
- If there is an applicable color scheme (CSV for Tk, CSS or CSV for 
  SVG) and a tile neither has its own color assigned nor belongs to 
  a group with a defined color, it will be white with black text to 
  make it easy to identify tiles with missing colors. 
- If there is no applicable color scheme, colors will be randomly 
  assigned to each group or top-level tile.

## Modular assignment of function 

- The main program (`treemap.py`) will collect command-line 
  arguments and open the color specification files if provided, so 
  that the main program can also produce appropriate error messages 
  for missing files. 
- To free the `mapper` module, whose concern is layout, from being 
  entangled with color schemes, the 
  main program communicates color schemes to the `display` module 
  through a separate `treemap_options` module. 
- To the extent possible, the `display` module is oblivious to where 
  color schemes came from.  In particular, it does not distinguish 
  between a CSS color scheme read from a CSS file and one generated 
  from a CSV color scheme for Tk.
- To the extent possible, color choice should be factored out of the 
  medium-specific modules `tk_display` and `svg_display` and 
  localized in `display`.  In this way, lookup happens only once, 
  consistently.  (However, CSS specs override CSV color maps for the 
  SVG display, so a color decision made in the `display` module may 
  be ignored by the `svg_display` module.)

## Implementation constraints for an inheritance through inclusion

Scalable vector graphics (SVG) with cascading style sheets (CSS) 
provide inclusion-based inheritance:  An object within another 
object (like a tile or subgroup within a group in our application) 
can inherit colors and other graphical attributes from its enclosing 
group.  Tk does not.  To make the Tk display consistent with the SVG 
display, we must provide this inheritance behavior.

The initial (Summer 2024) implementation of treemaps kept a stack of 
color pairs in the `display` module.  Every group pushed a new color 
pair, and a color pair was popped at the conclusion of every group.  
A tile got a random color assignment if the stack was empty, and 
otherwise took the top of the stack as a color assignment.  This 
implementation assumes every group has a color assignment, which was 
an acceptable assumption since we randomly assigned color pairs to 
every group.  User-provided color assignments break this assumption. 

Keeping a stack to implement color assignments remains the right way 
to implement inheritance through the inclusion hierarchy, but we can 
no longer make every stack element be a color pair.  There are two 
options:  We could implement a special "unassigned" color pair, or 
we could keep a stack of labels (which may or may not have assigned 
colors) in place of a stack of color pairs.  In either case we must 
walk the stack to find the nearest enclosing object with a color 
assignment, so a solution without a special case for "unassigned" is 
preferable. 

## API change: Category as required argument

The summer 2024 version of the `display` module had the following 
definitions of `draw_tile` and `begin_group`: 

```python
def draw_tile(r: geometry.Rect,
              label: str | None = None,
              tags: list[str] | None = None):
    """Draw the tile (on both media).
     Displays on Tk (Python built-in graphics) and
     also writes corresponding graphics into buffer to
     produce corresponding SVG diagram which can be displayed
     in a web page, imported into a diagramming tool like
     Inkscape, OmniGraffle, Illustrator, etc.
     Tags can be used to indicate additional SVG classes for style sheets.
    """
```

```python
def begin_group(r: geometry.Rect, label: str | None = None):
    """A group contains multiple rectangular regions.
    Rendering may differ between SVG and Tk versions,
    but in both cases we want to show hierarchy.
    The optional label appears as a tool-tip in the SVG version.
    """
```

The SVG class was derived from _the first line of_ the label, 
essentially extracting the category from a string composed in 
`mapper`.  This was a mistake.  In multiple places we were gluing 
together a string in `mapper` and then ungluing them in one of the 
display modules.  Henceforth we will pass the category and 
explanation as separate arguments.  In addition, with provision for 
separate style specifications, the `tags` argument will be 
eliminated to simplify the API.  The revised signatures will be: 

```python
def draw_tile(r: geometry.Rect,
              key: str | None = None,
              value: str | None = None):
    """Draw the tile (on both media).
     Displays on Tk (Python built-in graphics) and
     also writes corresponding graphics into buffer to
     produce corresponding SVG diagram which can be displayed
     in a web page, imported into a diagramming tool like
     Inkscape, OmniGraffle, Illustrator, etc.
     `key`, if present, is normalized to become the class name
     for SVG CSS class and/or the Tk color assignment table. 
    """
```

```python
def begin_group(r: geometry.Rect, 
                key: str | None = None,
                value: str | None = None):
    """
    Begin a group of tiles. The `key` argument, if present, 
    is normalized to become the class name for SVG CSS and/or
    the Tk color assignment table.  The (key, value) pair may not
    be directly visible, but if either `key` or `value` is present
    it will be displayed as a tooltip in SVG.  
    """
```

Note that `begin_group` now includes a `value` argument that can be 
used to display summary information, if available to the `mapper` 
module.  




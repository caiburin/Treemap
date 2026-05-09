# Beyond Treemaps: Project Ideas

There are many other ways to extend this project.  Here are a few.  
Some of these are _much_ more challenging than completing the project.
They are not little "extra credit" extensions, but rather
full-blown projects on their own.  If you 
want to tackle one of them, I suggest first trying to devise a plan 
of attack on your own, and then discussing it with your instructor 
before diving in. 

## Ordered squarified treemaps

Consider the treemap illustration from
[an article in 2026-06-25 issue of the New York Times](
https://www.nytimes.com/interactive/2025/06/22/upshot/harvard-funding-cuts.html)
on research funding cuts at Harvard.

![Harvard research grants cancelled](img/NYT-harvard.png)

This treemap is "squarified" like ours, but notice how the regions 
are also ordered top-to-bottom, left-to-right by total size.  

- What would you need to change in `mapper.py` to order a squarified 
  treemap in this way? 

- If you made ordering _optional_ (otherwise presenting data in the 
  order it appears in the source file), what is the cleanest* way to 
  control that option?   You will need new option in the top-level 
  `treemap.py` source file;  how would you convey that option to the 
  part of `mapper.py` that either does or does not sort regions by 
  size? 

_*_ _clean_ is a property of great importance to software developers,
although it is not easy to define unambiguously.   Consider the 
extent to which adding and conveying this option makes other parts 
of the code _messy_, i.e., full of extraneous detail that interferes 
with understanding and maintenance.  A _clean_ approach minimizes 
complexity and facilitates future changes.  Adding one feature in a 
_clean_ way may not look much different than adding that feature in 
a messy or _hacky_ way, but consider what happens if you add seven 
features in a similar manner.  In a _clean_ approach, each feature 
adds only a tiny bit of extra complexity, while a _messy_ approach 
grows into a distracting pile or, worse, a tangle of interacting 
features. 

## Custom text formatting

Sometimes the label for a rectangle does not fit cleanly within that 
area.  You can see the ugly effects by making a treemap 
visualization of `data/Chap08.json`:  Text extends outside the boxes,
and even overlaps.  There are several tactics we might use to 
improve text display: 

- We could suppress the text (not print it) when it is too long.
- We could break it into multiple lines. 
- We could truncate it in some way that maintains enough to 
  distinguish one label from another.  For example,
  `directory-tree-vertical.png` might be shortened to
  `dir...cal.png` (preserving the beginning, end, and file
  extension).

The best approach depends on the content of the data.  For example, 
a shortening scheme that preserves file extensions only makes sense 
if the labels are file names. Instead of a fixed scheme for fitting 
text, what we really need is a _custom_ shortening scheme suited to 
a particular kind of data.  

Editing `mapper.py` for each data set is a poor solution. We want a 
version of the `layout` function (and the functions it calls) to be 
fixed even as the text formatting is customized.  In Python, one way 
to accomplish this is to pass a function as an argument to another 
function.  We can add a custom text formatting function as a new 
argument to the `layout` function. 

While we have been running `mapper.py` as a main program, it is 
designed to be used also as a module that can be imported into 
another main program.  This is where we could define a more 
customized text layout function, such as one specifically for 
shortening long file names. 

## User-defined color schemes

The `display` module of this project chooses colors randomly. Often 
they are ugly, and they never convey semantic information. You could 
make color choices based on a separate _style sheet_, which could be 
a dictionary with the same hierarchical structure as the data.  This 
would be particularly useful if you wanted to use a consistent color 
scheme for two treemaps to compare the distribution of values at one 
time with the distribution of values in the same categories at a 
different time.

## Comparable treemaps

If you want to compare treemaps of related data, you might also want 
to account for difference in total area and grouping.  Suppose, for 
example, we wanted to compare the distribution of student majors 
between different academic terms. Total enrollment between those 
terms might be different, so we might want to scale one of the 
overall dimensions (height or width of the treemap as a whole) 
accordingly.  We might also want to record the `bisect` decisions in 
one run and replay them in another, for consistent grouping. 

## Appropriate use of treemaps and other displays

Here is an open-ended mission for a student with a strong interest 
in data visualization and a willingness to study human perception. 

You can find many data analysis tools that offer treemap displays.  
If you read their documentation, you will find much of it devoted to 
warning against using treemaps inappropriately.  For example, 
a simple bar graph is much better than a treemap for making precise 
comparisons.  Consider how hard it is to see that vanilla and 
chocolate have the same area in the `tiny_categorical.json` data set: 

![Chocolate and vanilla are both 10](
img/tiny_categorical.svg)

On the other hand, treemaps can be useful for quickly grasping 
quantitative part/whole relationships, like seeing that the biomass 
of eukaryotes as a group are a very large fraction of the biomass of 
the oceans, or that students majoring in the natural sciences outnumber 
students majoring in the social sciences in a computing course, but 
are a smaller overall portion of the class than computing-related 
majors (CS, DSCI, MACS, and CIS).

Consider some specific _use_ for which a treemap could be 
used, and consider the perceptual and cognitive processing 
that task requires.  Critique the strengths and weaknesses of 
treemap visualization for _that specific use_.  Can you identify a 
way to ameliorate a weakness or enhance a strength?  Do not rely on 
introspection or speculation.  Also, don't accept advice found in 
documentation uncritically. There 
is a rich scientific literature 
on human perception and human computer interaction to draw on. 

## Alternative (accessible) media 

Here's a much bigger project that builds on the prior one, regarding 
appropriate use of treemaps.  This is more on the scale of an MS 
thesis than a class project, but if you are interested in user 
interface and especially in accessible computing, it is not too early 
to start thinking along these lines and building the knowledge you will 
need to build accessible interfaces as your software development 
skills grow.  

Considering the tasks that treemaps 
are used _appropriately_ for, what presentation could serve 
effectively for visually impaired (e.g., blind) users?   Consider 
at least tactile and audio displays.  Don't assume that it will be 
a simple translation of the treemap display to another medium. 

Start with the task, and make use of what you know or can learn 
about perception and cognition to devise displays that are suitable 
to _that task_ with available technology. For tactile displays, 
consider the capabilities and limitations of Braille printers 
(basically low resolution static bitmap displays), pin grid arrays
like [Graphiti](https://www.orbitresearch.com/product/graphiti-plus/)
(even lower resolution, and expensive, but dynamic), and tactile 
printing on [swell touch paper](
https://americanthermoform.com/product/swell-touch-paper/).

[Haptics](https://en.wikipedia.org/wiki/Haptic_technology)
(active touch) are distinct from tactile display, but 
might also be worth considering.  Currently haptics are used 
primarily for simple "simulated button" displays, e.g., simulating a 
button click on a trackpad that does not actually depress, or 
joystick "rumble". Several systems that integrate haptics into 
touchscreens are in development. 

The [International Conference on Audio Display](https://icad.org/)
is a rich source of ideas and experimental evidence regarding audio 
display.  

The [ACM SIGACCESS](https://www.sigaccess.org/)
[Conference on Computers and Accessibility](https://www.sigaccess.org/assets/)
is a source of recent research in accessible interfaces, including 
but not limited to accessibility for visually impaired users.  











# The Bisect Function: A Cautionary Tale

The first version of the Treemap project used an unnecessarily 
complicated approach for the `bisect` method.  It was correct, but 
it was not _obviously_ correct.  It did not require much more code 
than the current approach, but it was harder to write and harder to 
reason about.   It stayed in the HOWTO instructions for a year.  I 
realized it was the wrong approach only when testing the HOWTO by 
rewriting a sample solution in summer 2025.  

I am sharing that wrong direction here, now in a separate document, 
because it is illustrative of a common bug in human problem-solving: 
Once we commit to an approach, we become somewhat blind to 
alternatives.  If we can make our first approach work, we may never 
step back to see that a simpler and better approach was possible. At 
the end of this short document I'll make a couple suggestions for 
overcoming this blindness to alternative approaches. 

## The `bisect` function

`bisect` is a function that divides a list of at least two positive 
numbers into two parts, a 
prefix and a suffix, balancing their sums.  For example,
`bisect([1, 2, 3, 4]` should return `([1, 2, 3], [4]`), with sums 6 
and 4.  Splitting earlier as `([1, 2], [3, 4])` gives sums 3 and 
7, which is more imbalanced.  Splitting later as `([1, 2, 3, 4], 
[])` is also worse.

## Pursuing the wrong approach

My intuition was to scan the list, stopping when the sum of the portion 
scanned so far was at least half the sum of the whole list.
This often works.  For the example of `[1, 2, 3, 4]`, the whole list 
sums to 10, and `[1, 2, 3]` is the first prefix with a sum at least 
5, which we'll call the target.

The complication comes in deciding 
whether to split before or after the first element that brings the
sum to more than the target. Sometimes, as with `[1, 2, 3, 4]`, the 
element that tips us over the edge (3 in this case) belongs in the 
prefix.  Sometimes it belongs in the suffix.  Consider splitting
`[1, 1, 2, 1]`.  The target is 5/2, or 2.5.  `sum([1, 1])` is 2, 
less than the target, so `[1, 2, 2]` is the first prefix that exceeds
the target.  However, splitting into `([1, 2], [2, 1])` is obviously 
more balanced than splitting into `([1, 2, 2], [1])`.  

If we are committed, as I was, to searching for the first element 
that brings the prefix sum to at least the target, then what seems 
to be needed is deciding whether that middle element belongs in the 
prefix or suffix.  I was able to make that choice by computing a 
"badness" score for each alternative and choosing the least bad 
split.  It worked, and the code was not long, but it was not beautiful.

## What I missed

Computing a badness score was simple, clear, and efficient (just a 
subtraction and taking an absolute value).  Had I taken a step back, 
I could have seen that it was clearer to scan the list for a minimum 
"badness" instead of scanning for the first item that exceeded the 
target.  When I returned to the code and rewrote it a year later, 
that improvement was obvious.  I missed it originally because my 
focus on solving a problem in my first approach blinded me to 
alternatives.  I didn't see that, instead of _solving_ the problem 
of deciding which list to include the critical element in, I could 
_avoid_ the problem. 


## Insight from debugging

Debugging is a key 
challenge in software development.  Made-up examples are seldom 
useful in building debugging skill and insight.  Real experience 
with real bugs is more useful. 

The excessive time I spent debugging `bisect` 
was a strong clue that my approach was not the best.  Moreover, the 
debugging process helped me (finally) see a better approach.


I saw test results 
like these:

```commandline
Failed example:
    bisect([1, 2, 1])  # Equally bad either way; split before pivot
Expected:
    ([1], [2, 1])
Got:
    ([1, 2], [1])
DEBUG:__main__:Bisecting [6, 5, 4, 3, 2, 1]
DEBUG:__main__:Bisecting [1, 2, 3, 4, 5]
**********************************************************************
File "/Users/michal/Dropbox/25F-210/projects/Treemap/mapper.py", line 75, in __main__.bisect
Failed example:
    bisect([1, 2, 3, 4, 5])
Expected:
    ([1, 2, 3], [4, 5])
Got:
    ([1, 2, 3, 4], [5])
```

A good debugging tactic is to start with the smallest failing
test case or the most 
obvious and easiest to fix error.  The first of these test cases,
`[1, 2, 1]`, is easy to understand:  Splitting as
`[1, 2], [1]` or splitting as `[1], [2, 1]` are equally bad,
but I had made an arbitrary decision to split before the "pivot" 
element that could go in either half.  (At least I resisted the
temptation to just change the test case.)  I suspected that some 
comparison `<=` or `>=` should be
`<` or `<`, or vice versa, but the test case is short enough that 
it was worthwhile to check my logic by working it through by hand.
I scribbled this little table on paper: 

target: `4/2 = 2`

 element  | 1  |  2  | 1 |
----------| ---| ---| --- |
 partial  |  1 |  3 | 4   |
 badness  |  1 |  1 | 2  |

We can see that the second element (at index 1) is the first element 
with a partial sum that exceeds the target, and the last element 
before the badness score starts increasing.  I could still try 
changing a line of my code from 

```python
        if partials[i] >= target:
```

to 

```python
        if partials[i] > target:
```

but it isn't obvious that this would be a real fix.
I am tempted to try it 
anyway, because it was my first guess and it's _so_ simple.
I did. I shouldn't have. It didn't help. 

Looking at the table, I had a strong impression that I should have 
been choosing an element that minimizes badness.   Let's consider 
the other failed test case, ` [6, 5, 4, 3, 2, 1]`, to see if that 
pattern holds. 

target: `15/2 = 7.5`

 element  | 1   | 2   | 3   | 4   | 5   |
----------|-----|-----|-----|-----|-----|
 partial  | 1   | 3   | 6   | 10  | 15  |
 badness  | 6.5 | 4.5 | 1.5 | 2.5 | 7.5 |

This is a clear minimum of badness when we split the list
as `[1, 2, 3], [4,5]`, even though the first partial sum
exceedng the target is `4`.  Perhaps with 
careful reasoning I could still 
find a way to make my code work using only the partial sums,
but selection using `badness` is much more clear and obvious.
_Obvious_ correctness is good.  

Voila! Small test cases that I can check by hand were essential to 
seeing that the right approach.  Using `badness` is simple, but 
_simple_ is not the same as _easy_.  In fact, finding the _simple_ 
solution that is _obviously_ correct can be hard!  The 
temptation to make small changes to code rather than working an 
example by hand is strong.  Working the example on paper to
find a solution that is _obviously_ 
correct is better in the long run. 

## How to do better

This is not the first time commitment to an approach has blinded me 
to alternatives, and it is unlikely to be the last.  It's a common 
weakness of human problem-solving behavior.   Nor can we avoid it 
entirely.  If we flit among several approaches to solving a problem 
rather than focusing on one, we are likely to become stuck and 
confused.  But we can recognize this vulnerability and take measures 
to improve.

### Backing out of blind alleys

Sometimes you will commit to an approach and become stuck.  You 
should not give up _too_ quickly.  But when an approach becomes too 
complicated, or you are unable to make progress, sometimes it is best 
to take a step back and reconsider basic approaches.  Even if you 
abandon your first approach, you may find that your effort to 
resolve its difficulties provides useful insight for another 
approach.  (The `badness` function that I wrote to simplify my 
initial approach helped me see, eventually, that it was really all I 
needed.)

### Fresh eyes

Sometimes you will be able to see an improved approach if you review 
your work after a walk, a nap, or a good night's sleep.  
Occasionally it could be upon returning to a project after a long 
time, as it was for me in this case.

The fresh eyes don't have to be your own.  There are many good 
reasons for asking another programmer (maybe a classmate) to read 
and critique your code.  Sometimes they spot bugs or suggest small 
improvements to clarity or efficiency.  Sometimes they can ask you 
key questions, like "why don't you just look for minimum badness?".  
There is a reason all the large successful software organizations 
make peer review of code a standard practice.

While asking your classmates or coworkers to serve as your fresh 
eyes, be willing to serve as theirs.  Your experience helping them 
improve their code will also help you write better code. 

### Develop an eye for elegance

Sometimes you are rushing to meet a deadline, whether it be to turn 
in an assignment or ship a product or add a feature requested by a 
client.  Sometimes "it works" has to be good enough.  

But when we 
can, we should aim for more than just working, adequate code.  We 
should aim for code that is as clear as possible.  It should not 
just be correct, but _obviously_ correct.   Achieving simplicity is 
not easy, but it should _look_ easy to another programmer reading 
the code.  That's elegance.  

You may not achieve it on the first try.  I often don't.  But aim 
for elegance, especially in code you revisit after some time away, 
especially in code you reuse across many applications, and most 
especially in code that other programmers use.   
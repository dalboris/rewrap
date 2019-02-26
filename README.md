# Rewrap

A plugin for Sublime Text to rewrap paragraphs.

You can install this plugin by adding the `Rewrap.py` file into your
`~/.config/sublime-text-3/Packages/User/` folder, then bind the `rewrap` command
to some shortcut (Preferences > Key Bindings), for example :

    [
        { "keys": ["alt+shift+q"], "command": "rewrap" },
    ]


# Description

Sublime Text has a built-in function to rewrap paragraphs, that is, to remove
and insert newlines so that lines are as long as possible without exceeding 80
characters (or any other user-defined max line length). This function can be
accessed in the menu under Edit > Wrap > Wrap Paragraph at Ruler
(<kbd>Alt</kbd><kbd>Q</kbd> in Windows and Linux,
<kbd>Command</kbd><kbd>Alt</kbd><kbd>Q</kbd> in OS X).

However, it doesn't always work like we expect. An alternative to the built-in
paragraph wrapper is [WrapPlus](https://github.com/ehuss/Sublime-Wrap-Plus), which
does a better job than the built-in function in many situations.

However, in some situations, neither the built-in function nor WrapPlus does
what I expect. More precisely, I find their definition of "paragraph" to be
often too liberal, wrapping stuff that I want to be left untouched. In
particular, they both ignore indentation, while I believe that a change of
indentation is a strong hint that we shouldn't keep wrapping past the change.

For example, consider the following text, where we want to wrap the first line:

    Since we know that we have this extremely beautiful relation below between x and y:
       x = y + 2
    We can deduce that:
       2*x = 2*y + 4

Result when using the built-in function:

    Since we know that we have this extremely beautiful relation below between
    x and y:     x = y + 2 We can deduce that:     2*x = 2*y + 4

Result when using WrapPlus:

    Since we know that we have this extremely beautiful relation below between x
       and y: x = y + 2 We can deduce that: 2*x = 2*y + 4

Result when using Rewrap (this plugin):

    Since we know that we have this extremely beautiful relation below between x
    and y:
       x = y + 2
    We can deduce that:
       2*x = 2*y + 4

As you can see, Rewrap didn't touch any of the lines starting with `x = y + 2`,
since a change of indentation has been detected.


# Key Features

**Conservative wrapping:** Only wraps adjacent non-blank lines with the exact
same prefix and indentation. Allowed prefix characters are `#`, `/`, `*`,
whitespaces and tabs, so this works with the following comment style:

    // Some multi-line
    // comment

    /// Some multi-line
    /// comment

    # Some multi-line
    # comment

    /*                     <- or Doxygen-style /** or /*!
     * Some multi-line
     * comment
     */

    /*
      Some multi-line
      comment
     */


**Remove duplicate whitespaces:** If there are duplicate whitespaces (e.g., two
consecutive whitespace characters), those will be removed. Those can occur if
you get paragraph justified with emacs for example,  with uses extra
whitespace for justification. They also occasionally occur when doing mistakes in
manually rewrapping a paragraph. None of the built-in function or WrapPlus cleans
these duplicate whitespaces, although sometimes this is what you may want.

**Preserve cursor position:** In many situations (not all), the cursor position
stays where it was before the wrap. Both the built-in function and WrapPlus place
the cursor at the end of the paragraph after rewrapping.


# Disclaimer

This plugin is very young, it doesn't have much functionality yet. It only works
in the most basic situations (for example, it does not work well with bulleted
or numbered lists), but at least it is very conservative in its definition of
paragraph, and is unlikely to wrap *more* than you want. It is quite likely to
wrap less than you want, though.

I personally have the following key bindings:

    { "keys": ["alt+q"], "command": "wrap_lines" },
    { "keys": ["alt+ctrl+q"], "command": "wrap_lines_plus" },
    { "keys": ["alt+shift+q"], "command": "rewrap" },

Which allows me to easily try all of three methods: the built-in rewrap
functionality, WrapPlus, and Rewrap. There's usually one of the three that does
what I want.


# Limitations with C-style comments

Currently, Rewrap doesn't work correctly if your comment starts at the first
line of C-style comment. Example:

        /* Let's try to wrap this long line with Rewrap and see what happens just for fun because why not!
         */

Becomes:

         /* Let's try to wrap this long line with Rewrap and see what happens
         /* just for fun because why not!
          */

In these situations, you can either use the built-in wrapper, or use WrapPlus,
or simply delete the added `/`. Note that if your comment was already
multi-line, you can simply trigger the `rewrap` command while having the cursor
in the second line or subsequent lines. It won't add superfluous `/*`, but
unfortunately it will leave the first line untouched. Example:

        /* Let's try
         * to wrap this long line with Rewrap and see what happens just for fun because why not!
         */

Becomes:

        /* Let's try
         * to wrap this long line with Rewrap and see what happens just for fun
         * because why not!
         */


# Todo

- Use user-defined max line length instead of our hardcoded `80`.
- Support bulleted or numbered lists.
- Support more comment styles. Currently, only three characters (`#`, `/`, and `*`)
  are considered prefixes.
- Better support C-style multiline comments, doxygen syntax, and other cases
  where the "prefix characters" are different for the first line than the other
  lines of the paragraph.
- Package with Package Control
- Have an option to let the user decide whether duplicated whitespaces should be
  removed.

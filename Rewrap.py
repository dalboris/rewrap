# File: Rewrap.py
# Author: Boris Dalstein
# License: Apache 2.0
#
# Terminology:
# - line:
#     a Region that contains exactly a single line of text.
# - paragraph:
#     a Region that starts at the beginning of a line,
#     and ends at the end of a line.
# - prefix:
#     part of the line before the actual words to wrap. For example, for the
#     line `// Some comment`, the prefix is `// `, including the whitespace.
# - direction:
#     an integer equal to either -1 or +1, specififying whether to search for
#     lines above the current Region (-1) or below the current Region (+1).
#

import sublime
import sublime_plugin
import re

def _computePrefix(string):
    prefixCharacters = "#/* \t"
    prefix = ""
    for c in string:
        if c in prefixCharacters:
            prefix += c
        else:
            break
    return prefix

def _hasLineAbove(view, paragraph):
    return paragraph.begin() > 0

def _getLineAbove(view, paragraph):
    return view.line(paragraph.begin() - 1)

def _hasLineBelow(view, paragraph):
    return paragraph.end() < view.size() - 1

def _getLineBelow(view, paragraph):
    return view.line(paragraph.end() + 1)

def _hasLine(view, direction, paragraph):
    if direction:
        return _hasLineBelow(view, paragraph)
    else:
        return _hasLineAbove(view, paragraph)

def _getLine(view, direction, paragraph):
    if direction > 0:
        return _getLineBelow(view, paragraph)
    else:
        return _getLineAbove(view, paragraph)

def _extend(view, direction, paragraph, prefix):
    while _hasLine(view, direction, paragraph):
        line = _getLine(view, direction, paragraph)
        string = view.substr(line)
        prefix2 = _computePrefix(string)
        if prefix2 == prefix and len(string) > len(prefix2):
            paragraph = paragraph.cover(line)
        else:
            break
    return paragraph

def _getParagraphAndPrefix(view):
    # Get current line and prefix
    currentPoint = view.sel()[0].begin()
    currentLine = view.line(currentPoint)
    prefix = _computePrefix(view.substr(currentLine))

    # Get paragraph by extending region above and below
    paragraph = _extend(view, +1, currentLine, prefix)
    paragraph = _extend(view, -1, paragraph, prefix)
    return paragraph, prefix

def _wrapParagraph(view, paragraph, prefix):
    # Remove prefixes and newlines; add a trailing whitespace
    lines = view.split_by_newlines(paragraph)
    text = ""
    for line in lines:
        string = view.substr(line)
        text += string[len(prefix):] + ' '

    # Remove duplicate whitespaces
    text = re.sub(' +', ' ', text)

    # Wrap text
    # TODO: change '80' by user's wrap width.
    maxLineLength = 80 - len(prefix)
    wtext = []
    wordStartPos = 0
    currentPos = 0
    for c in text:
        if c == ' ':
            word = text[wordStartPos:currentPos]
            if not wtext:
                wtext.append(word)
            elif len(wtext[-1]) + 1 + len(word) <= maxLineLength:
                wtext[-1] += ' ' + word
            else:
                wtext.append(word)
            wordStartPos = currentPos + 1
        currentPos += 1

    # Add prefixes and newlines
    sep = ''
    res = ""
    for wline in wtext:
        res += sep + prefix + wline
        sep = "\n"
    return res

class RewrapCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        paragraph, prefix = _getParagraphAndPrefix(view)
        wrappedParagraph = _wrapParagraph(view, paragraph, prefix)
        view.replace(edit, paragraph, wrappedParagraph)

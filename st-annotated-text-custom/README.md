# Annotated Text Component for Streamlit

# A slightly customized version of st-annotated-text. I removed the label part of the annotation - Liam Croteau

A simple component to display annotated text in Streamlit apps. For example:

![Example image](https://github.com/tvst/st-annotated-text/raw/master/example.png)

## Installation

First install Streamlit (of course!) then pip-install this library:

```bash
pip install streamlit
pip install st-annotated-text
```

## Example

```python
import streamlit as st
from annotated_text import annotated_text

annotated_text(
    "This ",
    ("is", "verb"),
    " some ",
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    "."
)
```

And you can customize colors:

```python
annotated_text(
    "This ",
    ("is", "verb", "#8ef"),
    " some ",
    ("annotated", "adj", "#faa"),
    ("text", "noun", "#afa"),
    " for those of ",
    ("you", "pronoun", "#fea"),
    " who ",
    ("like", "verb", "#8ef"),
    " this sort of ",
    ("thing", "noun", "#afa"),
    "."
)
```

## Parameters

The `annotated_text()` function accepts any number of the following arguments:

- strings, to draw the string as-is on the screen.
- tuples of the form (main_text, annotation_text, background, color) where
  background and foreground colors are optional and should be an CSS-valid string such as
  "#aabbcc" or "rgb(10, 20, 30)"
- [htbuilder.HtmlElement](https://github.com/tvst/htbuilder) objects in case you want to customize
  the annotations further. In particular, you can import the `annotation()` function from this
  module to easily produce annotations whose CSS you can customize via keyword arguments.

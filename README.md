# !!BANG!!

A text processor / static website generator.

💥 Put holes through text files 💥

[Preview](http://breadmakesyoufull.github.io/Bang/)

Bang comprises of a minimal markup language,
and a short python script.
For processing text replacements
in modular files.

Language: Python, Bang markup

Licence: MIT

Learn more:

* https://github.com/breadmakesyoufull/bang
* https://jamstack.org/generators/bang/
* https://staticgen.com

## Requires

* python 3
* bash

## Quickstart


```
# Process example files and open in web browser
./run.sh
```


## Bang markup syntax

### keyword definitions

Assignment Operators:

    !    - for assigning a word or line of text to a !!keyword!!
    !!   - for assigning file contents to a !!keyword!!
    !!!  - for assigning the return value of a shell commmand to a !!keyword!!

### keyword replacement

Keywords are enclosed in exclamation marks ``!!``, a.k.a double bangs

    !!keyword!!

This allows us to replace text with variables:

```
/* style.css */

* {
  background-color: !!bg_colour!!;
  colour: !!color!!;
  font-family: !!font!!;
}
```

And for text files to be modular:

```
<!-- index.html -->
!!html_start!!
!!head!!
!!body!!
!!html_end!!
```

## Process individual files

Process a text file:
```
./bang.sh markup.bang in/example.txt > out/example.txt
```

Process a webpage:
```
./bang.sh markup.bang in/index.html > out/index.html
```

## Process multiple files

You can chain standard bash utilities for processing multiple files.

See ``run.sh``

## Extra notes

This version, v2.0.0, is a much simplified re-implementation. You can still access v1.0.0 [here](https://github.com/BreadMakesYouFull/Bang/tree/1.0.0)

["broken glass 2" by Nesster](https://openverse.org/image/bbe0a83f-9b7f-488e-a7f5-4e6df7927fa0?q=glass) is licensed under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/?ref=openverse.)

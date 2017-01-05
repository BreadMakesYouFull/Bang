!!BANG!!
========
A text processor and static website generator.
Bang lets you shoot holes through text files!

Language: Python, custom (Bang script)

Templates: custom (Bang markup)

Licence: MIT

Bang comprises of an extremely minimalist markup language
and a quirky scripting language that can be extended with Python.
The Bang processor itself is a short Python script 
that interprets Bang scripts and processes text files. 
This allows for variables in text files,
as well as encouraging very modular text files.
The markup language allows you to shoot holes in text files 
with a double Bang enclosed keyword (eg: !!keyword!!).
Keywords are then then filled with a word, line of text, text file, 
or Python function return value. 
Bang scripts define the values of keywords, which files will be processed
and the order they will be processed in.
Text files should be utf-8 encoded.

![Bang logo](extra/logo.png "Bang logo")

--------------------------------------------------------------------------------

Requirements
------------
 - Python 3.1+

Installation
------------
1) Download Bang.

2) Place Bang in the directory you wish to use for your project.

Relative to your project directory bang.py should be located at:

    ./Bang/bang.py

3) To learn how to use Bang, you should read the quickstart guide below 
and the [user manual](./user_manual.markdown).

--------------------------------------------------------------------------------

Project Folder structure
------------------------
    .
    ├── Bang
    |   ├── scripts
    |   |   ├── <script_name>.bang
    :   |   └── global.bang
    :   ├── LICENSE.txt
    :   ├── README.markdown
    :   └── bang.py
    :
    Project files and folders 
    (No enforced structure)

Encoding and filetype
---------------------
All files processed by Bang should be utf-8 encoded.
They may have any (or no) extension:
 - .txt
 - .css 
 - .html 
 - .py

Bang scripts must have the extension:
 - .bang

--------------------------------------------------------------------------------
Quickstart
----------
The simplest way to process text with Bang is as follows:

1) Place Bang folder in the desired project directory as described in above in Installation.

2) Create text files of desired utf-8 encoded file format anywhere in the project.

3) Replace sections of text files with Bang keywords.

Keywords are enclosed in double bangs or exclamation marks (!!)

    !!keyword!!

This allows us to replace text with variables. For example, 

./css/style.css:

    body
    {
      background-color: !!bg_colour!!;
		  colour: !!color!!;
		  font-family: !!font!!;
    }

It also allows for text files to be very modular. For example,

./html/index.html:

    !!head!!
    !!body!!

4) Define the value of keywords in a Bang script, 
and specify what and when text files need to be processed.
For a more detailed description read the [user manual](./user_manual.markdown).

The easiest way to use Bang is to use a single global Bang script with global variables.

This file path of this script should be the following:

    <project_path>/Bang/scripts/global.bang

The scripting language has five operators, all of which consist of bangs.
Three of these assign a value to a keyword, and two are for file processing.

Assignment Operators:

    !    - for assigning a word or line of text to a !!keyword!!
    !!   - for assigning file of text to a !!keyword!!
    !!!  - for assigning the return value of a python script to a !!keyword!!

File processing operators:

    !!!! - for processing markup files, looking for and replacing !!keywords!!
    !!!!! - for wrapping text from a file around an existing file.

Here is the full list of legal Bang scripting language statements:

    !keyword string
    !!keyword file
    !!!keyword script arguments
    !!!! source/file.ext destination/file.ext
    !!!! source/*.ext destination/*.ext
    !!!! source/*.ext destination/name.ext preview.ext
    !!!! source/*.ext destination/name.ext preview.ext num
    !!!!! wrapper.ext target.ext
    !!!!! wrapper.ext target_directory/*.ext
    This is a comment

Here is an example global Bang script:

./Bang/scripts/global.bang:

    Lines that don't begin with ! are a comment.
    
    Assign values to keyword identifiers 
    (single bang for keyword = text)
    !bg-color rgb(0,0,0)
    !color rgb(255,255,255)
    !font serif
    
    Assign text from file to keyword identifiers
    (double bang for keyword = text from file)
    !!head html/head.html
    !!body html/body.html
    
    If ./html/body.html also contained Bang keywords, they could also be defined.
    (single bang for keyword = text)
    !body-heading
    !body-text 
    
    Process file with the defined keywords and save result in new location.
    (quadruple bang for processing text with the defined keywords)
    !!!! css/style.css site/style.css
    !!!! html/index.html site/index.html

--------------------------------------------------------------------------------

For a full explaination of the Bang scripting language read the [user manual](./user_manual.markdown).
This includes information about processing multiple files, 
variables scope, order of execution, document links and text wrappers.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
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
"""

#-------------------------------------------------------------------------------
# In-built python modules
#-------------------------------------------------------------------------------
# Used to find paths.
import os
import sys
# Sleep when the program is used in recursive mode.
from time import sleep, time
# Needed to run python scripts dynamically.
import importlib

#-------------------------------------------------------------------------------
# Path functions and file manipulation.
#-------------------------------------------------------------------------------
def path(file=sys.argv[0], path_name=False):
  """ 
  Returns the path of a file.

  If no file is given, the path of this script is returned.

  Args:
    relative (str): The relative pathname of the file or folder. (Default: __file__)
    path_name (bool): If True, the path will include the basename of the file. (Default: False)
    
  Returns:
    The path of a file. (str).
  """
  path = os.path.dirname(os.path.realpath(file))
  if path_name:
    path = os.path.join(path, os.path.basename(file))
  return path

def file_from_path(path, extension=True):
  """
  Returns a filename (basename) from a path.
  Args:
    path (str): The path including filename.
    path_name (bool): If True, the extension will be included. (Default: True)
    
  Returns:
    The filename (basename) of a path. (str).
  """
  file = os.path.basename(path)
  if not extension:
    file = os.path.splitext(file)[0]
  return file

def extension_from_path(path_name):
  """
  Returns an extension from a pathname.
  Args:
    path_name (str): The path including filename.
  Returns:
    The extension of a path. (str).
  """
  return os.path.splitext(os.path.basename(path_name))[1]

def project_path():
  """ Returns the path of the bang project. """ 
  return path(path())

def bang_scripts_path():
  """ Returns the directory of bang's scripts """
  try:
    with open(os.path.join(path(), "config.txt"), encoding="utf-8", mode="r") as config:
      return os.path.realpath(os.path.join(path(),config.read()))
  except FileNotFoundError:
      return os.path.join(path(), "scripts")

def find_bang_scripts():
  """ 
  Returns all bang files in the ./Bang/scripts directory in alphanumeric order.
  
  Returns:
    A list of bang files.
  """
  path = bang_scripts_path()
  files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".bang")]
  files = sorted(files)
  print("\nFound bang scripts:\n" + "\n".join(files))
  return files

def create_directory(path):
  """
  Creates a directory if it does not already exist.
  
  Args:
    path (str): The path to create.
  """
  if not os.path.exists(path):
    os.makedirs(path)

#-------------------------------------------------------------------------------
# Python extension
#-------------------------------------------------------------------------------
def run_python(script, *args, **variables):
  """
  Run a python script by module name and return its value.
  The module must contain a main(*args, **kwargs) function.
    
  Args:
    script (str): The script to run. 
    *args: arguments may be passed to pass to main() of script.
  Returns:
    The return value of script main(*args) function.
  """
  print("running: ", script)
  directory = path(os.path.join(project_path(), script))
  if directory not in sys.path:
    sys.path.append(directory)
  module = file_from_path(script, extension=False)
  print("p: ", directory, "\n", module, "\n")
  os.listdir(directory)
  module = importlib.import_module(module)
  value = module.main(*args, **variables)
  sys.path.remove(directory)
  return  value

#-------------------------------------------------------------------------------
# Process markup files
#-------------------------------------------------------------------------------
def find_markup(source, destination, file_or_extension, new_name=None, new_extension=None):
  """ 
  Finds markup files to process
  
  Args:
    source (str): The source folder of the markup file(s) location.
    destination (str): The destination folder of the markup file(s) location.
    file_or_extension (str): The markup file(s) to process.
    new_name (str): If a single file is being processed, it may be renamed. 
  
  Returns:
    tuple(input_files (list), output_files(list))  
  """
  # Check if we need to process one or several files.
  if file_or_extension[0] == ".":
    # Find multiple files to process, these will be moved but not rename.
    files = [file for file in os.listdir(source) if file.endswith(file_or_extension)]
    files = sorted(files)
    input_files = [os.path.join(source, file) for file in files]
    if new_extension:
      output_files = [os.path.join(destination, os.path.splitext(file)[0] + new_extension) for file in files]
    else:  
      output_files = [os.path.join(destination, file) for file in files]
  else:
    # Find the file to process and rename if needed.
    input_files = [os.path.join(source, file_or_extension)]
    if new_name:
      output_files = [os.path.join(destination, new_name)]
    else:
      output_files = [os.path.join(destination, file_or_extension)]
  return input_files, output_files

def check_markup(text, variables):
  """
  Check if the markup still needs processing.
  
  Args:
    text (str): text to check.
    variables (dict): A dictionary of variables (identifier: value).
  Returns:
    True if markup still contains keyword identifiers.
  """
  for identifier, value in variables.items():
    try:
      keyword = "!!" + identifier + "!!"
    except TypeError:
      # identifier is None or type other than a string.
      pass
    else:
      if (keyword in text):
        # Not all variables have been evaluated.
        # Text still needs processing.
        return True
  # All variables have been evaluated.
  # Text has finished processing
  return False

def evaluate_string(text, variables):
  """
  Evaluated a python string and replaces variable identifiers with values.
  
  Args:
    text (str): text to process.
    variables (dict): A dictionary of variables (identifier: value).
  Returns:
    Processed String.
  """
  while check_markup(text, variables):
    for identifier, value in variables.items():
      try:
        keyword = "!!" + identifier + "!!"
      except TypeError:
        # identifier is None or type other than a string.
        pass
      else:
        if value == None:
          # If variable is unassigned, set it to a blank string.
          value = ""
        text = text.replace(keyword, value)
  return text

def evaluate_markup(input_file, output_file, variables):
  """
  Evaluates bang markup file(s), and saves the output.
  
  Args:
    input_file (str): The markup file to evaluate.
    output_file (str): The output file.
    variables (dict): A dictionary of variables (identifier: value).
    new_name (str): If a single file is being processed, it may be renamed.
  """
  with open(input_file, encoding='utf-8', mode="r") as file:
    input_text = file.read()
    output_text = evaluate_string(input_text, variables)
  with open(output_file, encoding='utf-8', mode="w") as file:
    file.write(output_text)
    print("Saved:", output_file)

def process_markup(source, destination, file_or_extension, variables, new_name=None, reverse=False, format=None, new_extension=None):
  """
  Process bang markup file(s).
  
  Args:
    source (str): The source folder of the markup file(s) location.
    destination (str): The destination folder of the markup file(s) location.
    file_or_extension (str): The markup file(s) to process.
    variables (dict): A dictionary of variables (identifier: value).
    new_name (str): If a single file is being processed, it may be renamed. 
    reverse (bool): Reverse the file process order.
    format (str): The markup file that defines how to format the output.
  """
  # Find the markup file(s) we need to process.
  input_files, output_files = find_markup(source, destination, file_or_extension, new_name, new_extension)
  
  variables = variables.copy()
  
  if reverse:
    output_files = output_files[::-1]
  # Create a destination directory if it doesn't already exist.
  create_directory(destination)
  
  # Add navigation links if they have been defined
  if "<>" in variables and variables["<>"] != "":
    navigation = True
    back = "\n" + variables["<"]
    next = "\n" + variables[">"]
  else:
    navigation = False

  # Search for keywords in markup file(s) and replace them with thier assigned value.
  files = zip(range(0, len(input_files)), input_files, output_files)
  for i, input_file, output_file in files:
    variables["#"] = file_from_path(output_file)
    variables["##"] = file_from_path(output_file, extension=False)
    if format:
      snippet(input_file, output_file, format, variables)
    else:
      evaluate_markup(input_file, output_file, variables)
    
    # If navigation keywords are defined add links.
    if navigation:
      navigation_links = variables["<>"]
      
      if i != 0:
        name = file_from_path(output_files[i - 1], extension=False)
        ext = extension_from_path(output_files[i - 1])
        variables["#<"] = name + ext
        variables["<"] = back
      else:
        variables["<"] = ""
      if i != len(input_files)-1:
        name = file_from_path(output_files[i + 1], extension=False)
        ext = extension_from_path(output_files[i + 1])
        variables["#>"] = name + ext
        variables[">"] = next
      else:
        variables[">"] = ""

      with open(output_file, encoding="utf-8", mode="r") as file:
        text = evaluate_string(navigation_links, variables).replace("!!!!!", file.read())
      with open(output_file, encoding="utf-8", mode="w") as file:
        file.write(text)

def snippet(input_file, output_file, format_file, variables):
  """
  Evaluates bang markup file(s), and saves a formatted output.
  
  input_file (str): The file to generate the snippet from.
  output_file (str): The file to save to.
  format_file (str): The markup file that defines how to generate the snippet.
  variables (dict): A dictionary of variables (identifier: value).
  """
  variables = variables.copy()
  with open(input_file, encoding="utf-8", mode="r") as input:
    try:
      text = input.read().splitlines()
    except UnicodeDecodeError:
      print("Input file is not utf-8 encoded!")
  with open(format_file, encoding="utf-8", mode="r") as format:
    format = format.read()
  for i in range(1,10001):
    keyword = "!!" + str(i) + "!!"
    if keyword in format:
      variables[str(i)] = text[i - 1]
  text = evaluate_string(format, variables)
  with open(output_file, encoding="utf-8", mode="w") as output:
    output.write(text)

def generate_preview(source, destination, extension, preview, variables, name, num=None, reverse=False):
  """
  Generate a preview file based on snippets of several text files.
  
  Args:
    source (str): The source folder of the text/markup file(s) location.
    destination (str): The destination folder of the text/markup file(s) location.
    extension (str): The filetype to process.
    preview (str): The template markup file that defines previews.
    variables (dict): A dictionary of variables (identifier: value).
    name (str): The name of the generated file. 
    num(int): the maximum number of previews per file.
    """
  # get files
  files = [file for file in os.listdir(source) if file.endswith(extension)]
  files = sorted(files)
  
  variables = variables.copy()
  
  if reverse:
    files = files[::-1]
  input_files = [os.path.join(source, file) for file in files]
  output_file = os.path.join(destination, name)
  create_directory(destination)
  
  # Determine line keyword variables in preview. May be between !!1!! and !!10000!!
  lines = set()
  preview_text = ""
  with open(preview, encoding="utf-8", mode="r") as preview_template:
    preview_text = preview_template.read()
    for i in range(1,10001):
      if "!!" + str(i) + "!!" in preview_text:
        lines.add(i)
 
  output_text = ""
  for input_file in input_files:
    with open(input_file, encoding="utf-8", mode="r") as input_text:
      variables["#"] = file_from_path(input_file)
      variables["##"] = file_from_path(input_file, extension=False)
      try:      
        input_text = input_text.read().splitlines()
      except UnicodeDecodeError:
        print("Input file is not utf-8 encoded!")
        input_text = "" 
      else:
        for line in lines:
          keyword = "!!" + str(line) + "!!"
          variables[str(line)] = input_text[line - 1]
    output_text += evaluate_string(preview_text, variables)
  
  if num == None:
    output_file = os.path.join(destination, name)
    with open(output_file, encoding="utf-8", mode="w") as file:
      file.write("\n" + output_text)
      print("Generated: ", output_file)

  # If num is defined, seperate pages and add links if they are defined.
  else:
    output_text = ""
    post = 1
    page = 1
    posts = len(input_files)
    max_pages = posts // num + (posts % num > 0)
    remainder = posts % num
    for input_file in input_files:
      with open(input_file, encoding="utf-8", mode="r") as input_text:
        try:      
          input_text = input_text.read().splitlines()
        except UnicodeDecodeError:
          input_text = ""
        finally:
          variables["#"] = file_from_path(input_file)
          variables["##"] = file_from_path(input_file, extension=False)
          for line in lines:
            keyword = "!!" + str(line) + "!!"
            variables[str(line)] = input_text[line - 1]
        output_text += evaluate_string(preview_text, variables)
        post += 1
        if post > num or (page == max_pages and post > remainder and remainder != 0):
          suffix = "_" + str(page)
          preview_name = file_from_path(output_file, extension=False)
          preview_extension = extension_from_path(output_file)
          preview_file = preview_name + suffix + preview_extension
          preview_filepath = os.path.join(destination,  preview_file)
          
          if "<>" in variables and variables["<>"] != "":
            navigation_links = variables["<>"]
            if page != 1:
              variables["#<"] = preview_name + "_" + str(page - 1) + preview_extension
            else:
              navigation_links = navigation_links.replace("!!<!!", "")
            if page != max_pages:
              variables["#>"] = preview_name + "_" + str(page + 1) + preview_extension
            else:
              navigation_links = navigation_links.replace("!!>!!", "")         
            output_text = evaluate_string(navigation_links, variables).replace("!!!!!", output_text)
            
          file = open(preview_filepath, encoding="utf-8", mode="w")
          file.write(output_text)
          file.close()
          print("Generated: ", preview_file)
          output_text = ""
          post = 1
          page += 1

def wrap_file(wrapper_file, target_file, variables):
  """
  Wraps a text file with another text file.
  
  wrapper_file (str): Wrapper text file, that should include the wrap keyword (!!!!!).
  target_file (str): Target file to wrap with text (will be overwritten).
  variables (dict): A dictionary of variables (identifier: value).
  """
  # If multiple files are to be wrapped, the function will call itself seperately for each file.
  if file_from_path(target_file, extension=False) == "*":  
    directory = path(target_file)
    extension = extension_from_path(target_file)
    files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(extension)]
    for file in files:
      wrap_file(wrapper_file, file, variables)
  # Wrap the target file.
  else:
    with open(wrapper_file, encoding="utf-8", mode="r") as wrapper:
      wrapper_text = wrapper.read().split("!!!!!")
    with open(target_file, encoding="utf-8", mode="r") as target:
      text = target.read()
    try:
      text = wrapper_text[0] + text + wrapper_text[1]
    except IndexError:
      print("COULD NOT WRAP: ", target_file)
      print("Please ensure wrapper files contain the wrap keyword: !!!!!") 
    else: 
      target = open(target_file, encoding="utf-8", mode="w")
      text = evaluate_string(text, variables)
      target.write(text)
      target.close()
      print("wrapped: ", target_file)

#-------------------------------------------------------------------------------
# Process Bang scripts
#-------------------------------------------------------------------------------
def interpret_bang(line, variables):
  """
  Interpret a line from a bang file
  
  Args:
    line (str): a bang statememt to interpret.
    
  return:
    identifier, value
  """
  # Convert line into a bang statement.
  # The first word is a bang command.
  command = line.split()[0]
  # All words after the first word are arguments.
  arguments = line[len(command)+1:].replace("\n", "")
  # The operation is determined by counting prefixed bangs.
  operator = "!" * command[:5].count("!")
  # The identifier is the command without the bang prefix.
  identifier = command[len(operator):]

  # Read and perform bang statement.
  if operator == "!!!!!":
    # Wrap a text file with another text file.
    arguments = arguments.split()
    wrapper = os.path.join(project_path(), arguments[0])
    target = os.path.join(project_path(), arguments[1])
    wrap_file(wrapper, target, variables)
    return None, None

  elif operator == "!!!!":
    # Process markup file(s)
    arguments = arguments.split()
    # Get the source file(s).
    source = os.path.join(project_path(), arguments[0])
    source_directory = path(source)
    source_file = file_from_path(source)
    
    # Get the destination file(s)
    destination = os.path.join(project_path(), arguments[1])
    destination_directory = path(destination)
    destination_file = file_from_path(destination)
   
    reverse = False
    if line[4] == "/":
      reverse = True
    
    # Process file(s).
    if file_from_path(source_file, extension=False) == "*":
      source_files = source_file[1:]
      extension = source_files
      if file_from_path(destination_file, extension=False) == "*":
        # multiple source and destination files.
        new_extension = extension_from_path(destination_file)
        if len(arguments) == 3:
          format = os.path.join(project_path(), arguments[2])
          process_markup(source_directory, destination_directory, source_files, variables, reverse=reverse, format=format, new_extension=new_extension)
        else:
          process_markup(source_directory, destination_directory, source_files, variables, reverse=reverse, new_extension=new_extension)
      else:
        # multiple source files single destination file
        preview = os.path.join(project_path(),arguments[2])
        name = os.path.basename(destination_file)
        try:
          num = arguments[3]
        except IndexError:
          generate_preview(source_directory, destination_directory, extension, preview, variables, name, reverse=reverse)
        else:
          num = int(num)
          generate_preview(source_directory, destination_directory, extension, preview, variables, name, num, reverse=reverse)
    else:
      # single source and destination file
      if len(arguments) == 3:
        format = os.path.join(project_path(), arguments[2])
        process_markup(source_directory, destination_directory, source_file, variables, new_name=destination_file, format=format)
      else:
        process_markup(source_directory, destination_directory, source_file, variables, new_name=destination_file)
    # Delete the wrapper keyword if it exists.
    return None, None

  elif operator == "!!!":
    # Run python script.
    script_name = arguments.split()[0]
    if len(arguments) > 1:
      script_arguments = [arg for arg in arguments.split()[1:]]
    try:
      del variables[None]
    except KeyError:
      pass
    return identifier, run_python(script_name, *script_arguments, **variables)

  elif operator == "!!":
    # Read a text file.
    file_name = arguments.split()[0]
    with open(os.path.join(project_path(), file_name), encoding='utf-8', mode="r") as file:
      return identifier, file.read()

  elif operator == "!":
    # Read word or line of text.
    return identifier, arguments

def run_bang(filename, global_variables=None):
  """ Run a bang script.
  
  Args:
    filename (str): The bang script to process.
    global_variables (dict): global variables (identifier: value) may be used. 
  Returns:
    The variables defined in the bang script 
  """
  variables = dict()
  variables["@"] = project_path()
  variables["."] =  "\n" 
  if global_variables:
    variables.update(global_variables)
  with open(filename, encoding='utf-8', mode="r") as file:
    for line in file:
      # Check if this line is a bang statement.
      if line[0] == "!":
        # Interpret and evaluate a bang command.
        identifier, value = interpret_bang(line, variables)
        variables[identifier] = value
  return variables
  
#-------------------------------------------------------------------------------
# Run !!Bang!!
#-------------------------------------------------------------------------------
def main():
  
  runtime = time()
  
  """ Runs all bang scripts. """
  # Search for all bang scripts in alphameric order.
  bang_scripts = find_bang_scripts()

  # If a global bang script exists, run it and return global variables.
  global_bang=""
  for script in bang_scripts:
    if os.path.basename(script) == "global.bang":
      global_bang = script

  global_variables = set()
  if os.path.isfile(global_bang):
      print("\nProcessing global bang script.\n")
      global_variables = run_bang(global_bang)
      # Remove the global bang script as it has now been processed.
      bang_scripts.remove(global_bang)

  # Process each bang file.
  num = len(bang_scripts)
  for script, i in zip(bang_scripts, range(0,num)):
    print("\nProcessing " + str(i+1) + "/" + str(num) + ": " + file_from_path(script)) 
    variables = global_variables.copy()
    run_bang(script, variables)
  
  runtime = round(time() - runtime, 1)
  
  # All bang scripts have been processed.   
  print("\nBang! Bang! All files have been processed. ({}s)".format(runtime))

if __name__ == "__main__":
  """ Main program entry point. Runs all bang scripts. """

  # Override print unless -v has been has been specified as command line argument (verbose.
  python_print = print
  if not "-v" in sys.argv:
    # Store the standard print function.
    def print(*args):
      """ Override print function for quiet mode. """
      output = "".join([str(arg) for arg in args]).replace("\n", "")
      line_length = 80
      if len(output) > line_length:
        output = output[:line_length-3] + "..."
      output = output + " " * (line_length - len(output))
      python_print(output, end="\r")


  # If -s has been specified as command line argument, run silently.
  if "-s" in sys.argv:
    def print(*args):
      return

  # If -r has been specified as command line argument, run repeatedly.
  if "-r" in sys.argv:
    while True:
      main()
      sleep(10)

  main()
  python_print()

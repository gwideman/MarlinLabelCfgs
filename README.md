marlin_label_config_examples
----------------------------
This program operates on files within the repo MarlinConfigurations, providing them with vendor and model information so that they can be distinguished from one another when copied or moved from the original directory structure. 

In the MarlinConfigurations repo, there is a directory tree following the pattern:
> examples/[vendor]/[model]/

...with some variation in the depth of subdirectories.

In the leaf subdirs are some or all of the following files: Configuration.h, Configuration_adv.h, _Bootscreen.h, and _Statusscreen.h.  These files lack a clear indication of the vendor and model the file pertains to, which makes them easy to mix up when copying them into an actual Marlin source code tree.

 This program inserts into those files a define as follows:
```C
#define STRING_CONFIG_EXAMPLES_DIR ("examples/[subdirs]")
```
Because [subdirs] generally corresponds to [vendor]/[model], this provides an label that uniquely identifies the file and its purpose.

This define is placed right after ```pragma once``` near the top of the file.

* This program just uses the subdir rather than trying to derive vendor and model, because in some cases the directory structure has more or less depth, possibly with model and submodel. I declined to try to second-guess that.

Usage
-----
1. Edit marlin_label_config_examples.py to set input_examples_dir and output_examples_dir
* If you set output_examples_dir = input_examples_dir, the program will modify the files in place to add the define statement.
* If the directories are different, the program will first copy all the files from the input to the output directories, as some directories include files other than the ones that this program modifies.

2. Run the program, typically:
```python marlin_label_config_examples``` or
```python3 marlin_label_config_examples```


Additional nuances
------------------
* It is safe to run this program more than once on the same file(s). The code looks for an existing instance of ```STRING_CONFIG_EXAMPLES_DIR``` and leaves it alone if it's already correct and at the expected location, otherwise replaces it.

* The assumes that the various config files are encoded in UTF-8. Many of the Configuration_adv.h files contain UTF-8-specific characters in connection with the TOUCH_UI_UTF8_xxx series of defines, for examples.

* The code saves files using Linux-style newlines. 




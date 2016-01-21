#ycm-flags
Flags generator for [YouCompleteMe][YCM] vim plugin.

##Why do I want to use it?
Personally I find it a little bit annoying that [YouCompleteMe][YCM] requires me to provide compilation flags by hand
each and every time I use it. And what about header files?
Previously I had to provide all the compilation flags implicitly for [YCM][YCM] to work while editing header files.
So I've decided that automatization is needed, and this "tool" is what I came up with.

This tool utilize a [YCM][YCM]'s ability to read a "compilation database", namely `compile_commands.json`,
and the tool tries its best to deduce the correct compilation flags for any header file in your project.

If the header stuff doesn't work for you, please take a look at the
[Header files](#header-files) section.

##How to use
First of all, you have to make sure that path to `compile_commands.json` is resolved correctly.
The tool relies on two facts:

1. You will put it in the `%YOUR-REPO%/ycm` directory.
1. The `compile_commands.json` file resides in the `%YOUR-REPO%/build` directory.
If it is not the case, please amend `_project_path` and `_compilation_database_folder` variables correspondingly
in the constructor of the `YcmFlags` class in the file [`ycmflags.py`](ycmflags.py).

By default the `_project_path` is calculated as the `ycmflags.py`'s path + `/../`,
and the `_compilation_database_folder` is the project path + `/build/`.

1. Create `ycm` directory in the root of your project.
1. Put [`__init__.py`](__init__.py) and [`ycmflags.py`](ycmflags.py) there.
1. In a directory where you want an autocompletion to work (it may be also the project's root),
put `.ycm_extra_conf.py` file with the following contents:

```python
import sys, os

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '%PATH-TO-YCM-DIR%')))

import ycmflags

def FlagsForFile( filename ):
    flags = ycmflags.YcmFlags()
    return flags.flags_for_file(filename)

```
Where `%PATH-TO-YCM-DIR%` is a relative or absolute path to the `ycm` directory you've just created.
Actually you can name it whatever you like, `ycm` is just an example.

##Tuning
As you can see at [`ycmflags.py`](ycmflags.py), the constructor accepts the following options:

1. `flags`. If you want to pass any additional flags, here you go, pass them as a `list`: `["-xc++", "-Werror"]`.
1. `additional_includes`. This option is for any additional include paths you want,
it is also a `list`: `["/usr/include/curl", "some-weird-stuff/headers"]`. Keep in mind that relative pathes are
resolved relatively to the project's root.
1. `default_file`. If provided, this option will be treated as a set `[file_name, additional_flags]`.
The `file_name` option will be used to get compilation flags for any file that is not in a compilation database.
It should be specified as a path relative to the project's root: `"source/main.cpp"`.
The `additional_flags` option will be used as its name says as a set of additional flags: `["-x", "c++"]`.

##Header files
The main idea behind deducing compilation flags for a header file is to find a corresponding source file.
If the file is found, then its flags are used (via the "compilation database").

You can take a look at the algorithm in the static method `find_source_for_header`:
it tries to locate a source file with the same name in the same path and in some subfolders (namely `source` and `src`).

For example, if you have a file `/project/clang.h`, the tool will try to look for the following files:

- `/project/clang.cpp`
- `/project/clang.c`
- `/project/src/clang.cpp`
- `/project/src/clang.c`
- `/project/source/clang.cpp`
- `/project/source/clang.c`

If it doesn't work for you, please feel free to amend it the way you like. Feedback is appreciated!

[YCM]: https://github.com/Valloric/YouCompleteMe

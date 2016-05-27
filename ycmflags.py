# -*- coding: utf-8 -*-

import os

import ycm_core
from clang_helpers import PrepareClangFlags


SOURCE_EXTENSIONS = {
    "c++": (
        ".cpp",
        ".cxx"
    ),
    "c": (
        ".c",
    )
}

PATH_FLAGS = (
    '-isystem',
    '-I',
    '-iquote',
    '--sysroot='
)


def find_file(root, filename):
    for root, _, files in os.walk(root):
        for f in files:
            if filename == f:
                return os.path.join(root, f)


def find_source_for_header(header):
    header_folder, header_name = os.path.split(header)
    base_name, header_ext = os.path.splitext(header_name)

    if header_ext not in (".h", ".hpp"):
        return header, []

    for lang in SOURCE_EXTENSIONS:
        for source_ext in SOURCE_EXTENSIONS[lang]:
            source_name = base_name + source_ext
            source = find_file(header_folder, source_name)
            if source is not None:
                return source, ["-x", lang]

    return header, []


class YcmFlags:
    """Flags generator for YouCompleteMe vim plugin"""

    def __init__(self, absolute_project_path=None, flags=None,
                 additional_includes=None, default_file=None, build_path="build/"):
        """See `README.md` for information about options"""
        if absolute_project_path is None:
            raise NameError('Please set up the `absolute_project_path` argument.')
        self._flags = flags if flags is not None else []
        self._default_file = default_file if default_file is not None else ()
        if isinstance(additional_includes, (tuple, list)):
            self._flags.extend(
                [["-I", include] for include in additional_includes])

        self._project_path = os.path.abspath(absolute_project_path)
        self._compilation_db_path = os.path.join(self._project_path, build_path)
        if os.path.exists(self._compilation_db_path):
            self._db = ycm_core.CompilationDatabase(self._compilation_db_path)
            if not self._db:
                raise NameError('Failed to prepare a compilation DB')
        else:
            raise NameError('No compilation DB!')

    @staticmethod
    def relative_to_absolute(flags, absolute_path):
        new_flags = []
        make_next_absolute = False
        for flag in flags:
            if make_next_absolute:
                make_next_absolute = False
                if not flag.startswith('/'):
                    new_flag = os.path.join(absolute_path, flag)
                else:
                    new_flag = flag
                new_flags.append(os.path.normpath(new_flag))
                continue
            new_flag = flag
            for path_flag in PATH_FLAGS:
                if flag == path_flag:
                    make_next_absolute = True
                    break
                if flag.startswith(path_flag):
                    path = flag[len(path_flag):]
                    new_flag = path_flag + os.path.normpath(
                        os.path.join(absolute_path, path))
                    break
            new_flags.append(new_flag)
        return new_flags

    def flags_for_default_file(self):
        if not self._default_file:
            raise NameError("No default flag set, so no flags extracted")

        source, flags = self._default_file
        compilation_info = self._db.GetCompilationInfoForFile(
            os.path.join(self._project_path, source))

        return (
            compilation_info,
            self.relative_to_absolute(flags, self._project_path)
        )

    def flags_for_file(self, filename):
        additional_flags = []
        source, extra_flags = find_source_for_header(filename)

        compilation_info = self._db.GetCompilationInfoForFile(source)
        if not compilation_info.compiler_flags_:
            compilation_info, additional_flags = self.flags_for_default_file()

        additional_flags.extend(
            self.relative_to_absolute(self._flags, self._project_path))

        flags = PrepareClangFlags(
            self.relative_to_absolute(
                compilation_info.compiler_flags_,
                compilation_info.compiler_working_dir_),
            source)

        return {
            'flags': flags + additional_flags + extra_flags,
            'do_cache': True
        }

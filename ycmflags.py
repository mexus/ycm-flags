import os
import ycm_core
from clang_helpers import PrepareClangFlags


class YcmFlags:
    def __init__(self, flags = [], additional_includes = []):
        self._flags = flags
        self._project_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
        self._compilation_database_folder = os.path.join(self._project_path, 'build/')
        if self._compilation_database_folder:
            self._database = ycm_core.CompilationDatabase(self._compilation_database_folder)
            if not self._database:
                raise NameError('Failed to prepare a compilation DB')
        else:
            raise NameError('No compilation DB!')
        for include in additional_includes:
            self._flags.extend(['-I', include])

    @staticmethod
    def find_source_for_header(filename):
        (base_folder, name) = os.path.split(filename)
        (base_name, extension) = os.path.splitext(name)
        # 0. Check if the file is a header:
        if extension not in {".h", ".hpp"}:
            return (filename, [])
        extensions = [["c++", ".cpp"], ["c++", ".cxx"], ["c", ".c"]]
        for pair in extensions:
            lang = pair[0]
            source_extension = pair[1]
            source_file_name = base_name + source_extension
            # 1. Look in the same folder and subfolders
            for subfolder_name in {"", "src", "source"}:
                sub_folder = os.path.join(base_folder, subfolder_name)
                if os.path.exists(sub_folder) and os.path.isdir(sub_folder):
                    probable_source = os.path.join(sub_folder, source_file_name)
                    if os.path.exists(probable_source):
                        return (probable_source, ["-x", lang])
        # 3. Give up
        return (filename, [])

    @staticmethod
    def relative_to_absolute(flags, absolute_path):
        new_flags = []
        path_flags = ['-isystem', '-I', '-iquote', '--sysroot=']
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
            for path_flag in path_flags:
                if flag == path_flag:
                    make_next_absolute = True
                    break
                if flag.startswith(path_flag):
                    path = flag[len(path_flag):]
                    new_flag = path_flag + os.path.normpath(os.path.join(absolute_path, path))
                    break
            new_flags.append(new_flag)
        return new_flags

    def flags_for_file(self, original_filename):
        (filename, extra_flags) = YcmFlags.find_source_for_header(original_filename)
        compilation_info = self._database.GetCompilationInfoForFile(filename)
        flags = PrepareClangFlags(
            self.relative_to_absolute(
                compilation_info.compiler_flags_,
                compilation_info.compiler_working_dir_),
            filename)
        additional_flags = self.relative_to_absolute(self._flags, self._project_path)
        flags.extend(additional_flags)
        return {
            'flags': flags + extra_flags,
            'do_cache': True
        }

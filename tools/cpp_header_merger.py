__author__ = 'Joshua Zhang'
"""A C/C++ header merging tool """

import os
import re
import argparse

# matching c/c++ #include patterns
pattern_include = r"#.*include.+(\.hpp|\.h)+"
pattern_squote = r"<.+>"
pattern_quote = r'".+"'
pattern_pragma = r"#pragma.+once"
regex_include = re.compile(pattern_include, re.IGNORECASE)
regex_squote = re.compile(pattern_squote, re.IGNORECASE)
regex_quote = re.compile(pattern_quote, re.IGNORECASE)
regex_pragma = re.compile(pattern_pragma, re.IGNORECASE)

# blacklist
black_list = set()

def custom_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--include', help='Include path for headers', required=True)
    parser.add_argument('-o', '--output', help='Output file path', required=False)
    parser.add_argument('-e', '--entry', help='Entry header file to start with', required=True)
    return parser

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line


def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)


def replace_nonsystem_header(line, file):
    if re.search(regex_include, line) is not None:
        if re.search(regex_squote, line) is not None:
            target = line.split('<')[-1].split('>')[0]
            if target in black_list:
                target = 'blacklist'
            else:
                target = os.path.abspath(include_path + target)
        elif re.search(regex_quote, line) is not None:
            target = line.split('"')[1]
            target = os.path.dirname(os.path.abspath(file)) + '/' + target
        else:
            raise Exception("Invalid #include header")

        target = os.path.abspath(target)
        if target not in history:
            history.add(target)
            return "/*" + line + "*/" + os.linesep + process_header(target)
        else:
            return "/*" + line + " skipped */"

    return line

def process_header(file):
    print("Processing: " + file)
    try:
        with open(file, "rb") as fnow:
            this_buffer = []
            require_guard = None
            # remove c/c++ comments
            lines_wo_comments = remove_comments(fnow.read())
            for line in nonblank_lines(lines_wo_comments.splitlines()):
                new_line = replace_nonsystem_header(line, file)
                if re.search(regex_pragma, new_line) is not None:
                    new_line = ""
                    require_guard = 1
                    tmp = file.lstrip(os.path.abspath(include_path)).upper().replace('/', '_').replace('.', '_')
                    this_guard_name = "_AUTOMATIC_GUARD_" + tmp + "_"
                    this_buffer.append("#ifndef " + this_guard_name + os.linesep + '#define ' + this_guard_name)
                this_buffer.append(new_line)
            if require_guard == 1:
                this_buffer.append("#endif /* END " + this_guard_name + " */")
            this_string = os.linesep.join(this_buffer)
            # print(this_string)
            return this_string
    except IOError:
        skipped_list.add(file.lstrip(os.path.abspath(include_path)))
        return ''


def merge_header(entry, output):
    with open(output, "wb") as fout:
        # open output for write
        result = process_header(entry)
        fout.write(result)
        print("Done.")

if __name__ == '__main__':
    parser = custom_parser()
    args = vars(parser.parse_args())
    entry_file = args['entry']
    include_path = args['include']
    output_file = args['output'] if args['output'] is not None else entry_file + "_out.hpp"
    history = set(['blacklist'])
    skipped_list = set()
    merge_header(entry_file, output_file)

    # print skipped files
    print("\nThe following files are skipped, should be system headers, otherwise there must have mistakes.")
    for skipped in skipped_list:
        print("***Unable to open file: " + skipped + ", skipped")

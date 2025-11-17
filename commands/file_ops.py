"""
File Operations Commands Module
Implements file reading and manipulation commands
"""


def execute_cat(vfs, args, print_func):
    """Execute cat command - concatenate and print files"""
    if not args:
        print_func("Usage: cat filename [...]")
        return

    # Read and display each file
    for filename in args:
        content, error = vfs.read_file(filename)
        if error:
            print_func(error)
        else:
            # Print file content (remove trailing newline if present to avoid double newlines)
            if content and content.endswith('\n'):
                content = content[:-1]
            if content:
                for line in content.split('\n'):
                    print_func(line)

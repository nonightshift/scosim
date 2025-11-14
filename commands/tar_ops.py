"""
Tar Archive Commands Module
Implements tar archive creation and extraction
"""

import io
import tarfile
from vfs import VNode


def execute_tar(vfs, args, print_func):
    """Execute tar command - create or extract tar archives"""
    if len(args) < 2:
        print_func("Usage: tar [cvf|xvf] file [directory]")
    else:
        options = args[0]
        tarfile_name = args[1]

        if options == "cvf":
            # Create tar archive
            if len(args) < 3:
                print_func("tar: missing directory argument")
            else:
                dir_path = args[2]
                target = vfs.resolve_path(dir_path)
                if target is None:
                    print_func(f"tar: {dir_path}: No such file or directory")
                elif not target.is_dir:
                    print_func(f"tar: {dir_path}: Not a directory")
                else:
                    # Create tar archive in memory
                    tar_content = _create_tar(target)
                    # Store as virtual file
                    tar_node = VNode(tarfile_name, is_dir=False)
                    tar_node.content = tar_content
                    tar_node.size = len(tar_content)
                    vfs.current_dir.add_child(tar_node)
                    # Print verbose output
                    _print_tar_contents(target, print_func, "a")

        elif options == "xvf":
            # Extract tar archive
            tar_node = vfs.resolve_path(tarfile_name)
            if tar_node is None:
                print_func(f"tar: {tarfile_name}: No such file or directory")
            elif tar_node.is_dir:
                print_func(f"tar: {tarfile_name}: Is a directory")
            else:
                # Extract tar archive
                if tar_node.content:
                    _extract_tar(vfs, tar_node.content, print_func)
                else:
                    print_func(f"tar: {tarfile_name}: Empty archive")

        else:
            print_func(f"tar: invalid option -- '{options}'")
            print_func("Usage: tar [cvf|xvf] file [directory]")


def _create_tar(root_node):
    """Create a tar archive from a virtual directory tree"""
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
        _add_to_tar(tar, root_node, root_node.name)
    return tar_buffer.getvalue()


def _add_to_tar(tar, node, arcname):
    """Recursively add nodes to tar archive"""
    info = tarfile.TarInfo(name=arcname)
    info.mtime = int(node.mtime.timestamp())
    info.uid = 0
    info.gid = 0
    info.uname = node.owner
    info.gname = node.group

    if node.is_dir:
        info.type = tarfile.DIRTYPE
        info.mode = 0o755
        tar.addfile(info)
        # Add children
        for child_name, child_node in node.children.items():
            child_arcname = f"{arcname}/{child_name}"
            _add_to_tar(tar, child_node, child_arcname)
    else:
        info.type = tarfile.REGTYPE
        info.mode = 0o644
        info.size = len(node.content) if node.content else 0
        content_bytes = node.content.encode('utf-8') if node.content else b''
        tar.addfile(info, io.BytesIO(content_bytes))


def _print_tar_contents(node, print_func, prefix="a", path=""):
    """Print tar archive contents in verbose mode"""
    current_path = f"{path}/{node.name}" if path else node.name
    print_func(f"{prefix} {current_path}")

    if node.is_dir:
        for child_name, child_node in sorted(node.children.items()):
            _print_tar_contents(child_node, print_func, prefix, current_path)


def _extract_tar(vfs, tar_content, print_func):
    """Extract a tar archive to the virtual filesystem"""
    tar_buffer = io.BytesIO(tar_content)
    try:
        with tarfile.open(fileobj=tar_buffer, mode='r') as tar:
            for member in tar.getmembers():
                # Print extraction (verbose mode)
                print_func(f"x {member.name}")

                # Skip if it's the root of the archive
                if not member.name or member.name == '.':
                    continue

                # Parse path
                path_parts = member.name.split('/')

                # Navigate to parent directory
                parent = vfs.current_dir
                for part in path_parts[:-1]:
                    if part not in parent.children:
                        # Create intermediate directory
                        new_dir = VNode(part, is_dir=True)
                        parent.add_child(new_dir)
                        parent = new_dir
                    else:
                        parent = parent.children[part]

                # Create the file or directory
                name = path_parts[-1]
                if member.isdir():
                    if name not in parent.children:
                        new_dir = VNode(name, is_dir=True)
                        parent.add_child(new_dir)
                else:
                    # Extract file content
                    file_content = tar.extractfile(member)
                    content = file_content.read().decode('utf-8') if file_content else ""

                    new_file = VNode(name, is_dir=False)
                    new_file.content = content
                    new_file.size = len(content)
                    parent.add_child(new_file)

    except Exception as e:
        print_func(f"tar: Error extracting archive: {e}")

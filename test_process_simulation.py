#!/usr/bin/env python3
"""
Test script for process simulation
"""

from process_table import ProcessTable, Process
from commands.info import execute_ps
from commands.process_ops import execute_kill


def test_process_table():
    """Test process table functionality"""
    print("=== Testing Process Table ===\n")

    # Create process table
    ptable = ProcessTable()

    print(f"Loaded {len(ptable.get_all_processes())} processes")
    print("\nSample processes:")
    for proc in list(ptable.get_all_processes())[:5]:
        print(f"  PID {proc.pid}: {proc.command} (user: {proc.uid})")

    # Test getting PP X.400 MTA processes
    print("\n\n=== PP X.400 MTA Processes ===")
    pp_processes = ptable.get_processes_by_command("/home/dxmail/pp/bin/")
    print(f"Found {len(pp_processes)} PP X.400 MTA processes:")
    for proc in pp_processes:
        print(f"  PID {proc.pid}: {proc.command}")

    return ptable


def test_ps_command(ptable):
    """Test ps command"""
    print("\n\n=== Testing ps Command ===\n")

    output = []
    def capture_output(text):
        output.append(text)

    # Test simple ps
    print("--- ps (simple) ---")
    execute_ps("root", [], capture_output)
    for line in output:
        print(line)

    # Test ps -ef
    output.clear()
    print("\n--- ps -ef (full listing) ---")
    execute_ps("root", ["-e", "-f"], capture_output)
    for line in output[:10]:  # Show first 10 lines
        print(line)
    print(f"... ({len(output)} total lines)")


def test_kill_command(ptable):
    """Test kill command"""
    print("\n\n=== Testing kill Command ===\n")

    # Get a PP process to kill
    pp_processes = ptable.get_processes_by_command("/home/dxmail/pp/bin/")
    if pp_processes:
        test_pid = pp_processes[0].pid
        print(f"Testing kill on PID {test_pid} ({pp_processes[0].command})")

        output = []
        def capture_output(text):
            output.append(text)

        # Test as root user (should succeed)
        execute_kill("root", [str(test_pid)], capture_output)
        if output:
            for line in output:
                print(f"  {line}")
        else:
            print(f"  Process {test_pid} terminated (silent success)")

        # Check if process is gone
        if ptable.get_process(test_pid) is None:
            print(f"  ✓ Process {test_pid} successfully removed from process table")
        else:
            print(f"  ✗ Process {test_pid} still exists!")

    # Test kill on non-existent process
    print("\nTesting kill on non-existent process (PID 9999):")
    output.clear()
    execute_kill("root", ["9999"], capture_output)
    for line in output:
        print(f"  {line}")


def test_queue_population():
    """Test that queues are populated"""
    print("\n\n=== Testing Queue Population ===\n")

    import json
    with open("filesystem.json", "r") as f:
        fs_data = json.load(f)

    def count_queue_messages(node, queue_name):
        """Recursively count messages in a queue"""
        if not isinstance(node, dict):
            return 0

        name = node.get("name", "")

        if name == queue_name and "children" in node:
            # Count .x400 files
            messages = [c for c in node["children"] if isinstance(c, dict) and c.get("name", "").endswith(".x400")]
            return len(messages)

        # Continue searching
        if "children" in node and isinstance(node["children"], list):
            for child in node["children"]:
                count = count_queue_messages(child, queue_name)
                if count > 0:
                    return count

        return 0

    in_count = count_queue_messages(fs_data, "in")
    out_count = count_queue_messages(fs_data, "out")

    print(f"In queue: {in_count} messages")
    print(f"Out queue: {out_count} messages")
    print(f"Total: {in_count + out_count} messages")

    if in_count + out_count >= 100:
        print("✓ Queue population successful!")
    else:
        print("✗ Queue population incomplete!")


if __name__ == "__main__":
    # Run tests
    ptable = test_process_table()
    test_ps_command(ptable)
    test_kill_command(ptable)
    test_queue_population()

    print("\n\n=== All Tests Complete ===")

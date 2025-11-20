#!/usr/bin/env python3
"""
Script to populate PP X.400 MTA queues with sample messages
Generates approximately 100 sample X.400 messages in the in and out queues
"""

import json
import random
from datetime import datetime, timedelta


def generate_x400_message_content(msg_id, sender, recipient, subject):
    """Generate sample X.400 message content"""
    return f"""Message-ID: {msg_id}
X400-Originator: {sender}
X400-Recipient: {recipient}
Subject: {subject}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Content-Type: text/plain

This is a sample X.400 message for testing purposes.
Message ID: {msg_id}
"""


def generate_sample_messages():
    """Generate sample message data"""
    messages = []

    # Sample senders and recipients
    senders = [
        "/C=DE/ADMD=DBP/PRMD=COMPANY/O=EXAMPLE/OU=SALES/S=Mueller/",
        "/C=DE/ADMD=DBP/PRMD=COMPANY/O=EXAMPLE/OU=IT/S=Schmidt/",
        "/C=DE/ADMD=DBP/PRMD=COMPANY/O=EXAMPLE/OU=HR/S=Weber/",
        "/C=US/ADMD=ATT/PRMD=ACME/O=CORP/S=Johnson/",
        "/C=GB/ADMD=BT/PRMD=UK-CORP/O=BRITISH/S=Smith/",
    ]

    recipients = [
        "/C=DE/ADMD=DBP/PRMD=PARTNER/O=CUSTOMER/S=Fischer/",
        "/C=DE/ADMD=DBP/PRMD=SUPPLIER/O=VENDOR/S=Wagner/",
        "/C=US/ADMD=ATT/PRMD=CLIENT/O=BUSINESS/S=Williams/",
        "/C=GB/ADMD=BT/PRMD=TRADE/O=PARTNER/S=Brown/",
        "/C=FR/ADMD=ATLAS/PRMD=FRENCH/O=SOCIETE/S=Martin/",
    ]

    subjects = [
        "Order Confirmation #",
        "Invoice ",
        "Meeting Request - ",
        "Product Information",
        "Delivery Notice",
        "Status Report",
        "Technical Documentation",
        "Contract Details",
    ]

    # Generate 100 messages
    base_time = datetime(1995, 12, 5, 8, 0, 0)

    for i in range(100):
        msg_num = i + 1
        msg_id = f"19951205{msg_num:04d}.AA{msg_num:03d}"

        sender = random.choice(senders)
        recipient = random.choice(recipients)
        subject = random.choice(subjects) + str(random.randint(1000, 9999))

        # Calculate message timestamp (spread over several days)
        msg_time = base_time + timedelta(hours=random.randint(0, 72), minutes=random.randint(0, 59))

        # Determine size (between 1KB and 20KB)
        size = random.randint(1024, 20480)

        messages.append({
            "name": f"msg{msg_num:04d}.x400",
            "is_dir": False,
            "permissions": "rw-r--r--",
            "owner": "dxmail",
            "group": "mail",
            "size": size,
            "content": generate_x400_message_content(msg_id, sender, recipient, subject),
            "mtime": msg_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    return messages


def find_queue_directories(data, path=""):
    """Recursively find the queue directories in the filesystem tree"""
    queue_dirs = {}

    if isinstance(data, dict):
        name = data.get("name", "")
        current_path = f"{path}/{name}" if path else name

        # Check if this is one of the queue directories we're looking for
        if name in ["in", "out"] and "/pp/queue" in path:
            queue_dirs[name] = data

        # Recursively search children
        if "children" in data and isinstance(data["children"], list):
            for child in data["children"]:
                child_dirs = find_queue_directories(child, current_path)
                queue_dirs.update(child_dirs)

    return queue_dirs


def populate_queues():
    """Main function to populate the queues in filesystem.json"""
    # Load filesystem.json
    with open("filesystem.json", "r", encoding="utf-8") as f:
        fs_data = json.load(f)

    # Generate messages
    all_messages = generate_sample_messages()

    # Split messages between in and out queues
    # 60 in the 'in' queue, 40 in the 'out' queue
    in_messages = all_messages[:60]
    out_messages = all_messages[60:]

    # Find queue directories
    def find_and_populate(node):
        """Recursively find and populate queue directories"""
        if not isinstance(node, dict):
            return False

        name = node.get("name", "")

        # Check if we found the pp/queue structure
        if name == "queue" and "children" in node:
            for child in node["children"]:
                if child.get("name") == "in":
                    child["children"] = in_messages
                    print(f"Added {len(in_messages)} messages to in queue")
                elif child.get("name") == "out":
                    child["children"] = out_messages
                    print(f"Added {len(out_messages)} messages to out queue")

        # Continue searching in children
        if "children" in node and isinstance(node["children"], list):
            for child in node["children"]:
                find_and_populate(child)

    # Populate the queues
    find_and_populate(fs_data)

    # Save updated filesystem.json
    with open("filesystem.json", "w", encoding="utf-8") as f:
        json.dump(fs_data, f, indent=2)

    print(f"Successfully populated queues with {len(all_messages)} messages")
    print(f"  - in queue: {len(in_messages)} messages")
    print(f"  - out queue: {len(out_messages)} messages")


if __name__ == "__main__":
    populate_queues()

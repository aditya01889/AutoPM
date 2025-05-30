"""Run the AutoPM demo"""
import asyncio
import sys
import os

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)

print("🚀 Starting AutoPM Demo")
print("-" * 40)
print("Python version:", sys.version)
print("Working directory:", os.getcwd())
print("Files in directory:", os.listdir('.'))

# Sample data to demonstrate functionality
sample_updates = {
    "slack": [
        "Team meeting scheduled for tomorrow at 10 AM",
        "New feature request from @alice: Add dark mode support",
        "Bug reported by @bob: Login page not loading on mobile"
    ],
    "jira": [
        "[PROJ-123] Implement user authentication - In Progress",
        "[PROJ-124] Fix login page layout - Done",
        "[PROJ-125] Add password reset feature - To Do"
    ],
    "notion": [
        "Project timeline updated: Phase 1 completion delayed by 2 days",
        "New document added: API Documentation v1.2",
        "Meeting notes from 2023-05-30 uploaded"
    ]
}

# Display sample updates
print("\n📋 Sample Updates from Different Sources:")
for source, updates in sample_updates.items():
    print(f"\n🔹 {source.upper()}:")
    for update in updates:
        print(f"   • {update}")

# Simulate AI summarization
print("\n🤖 Generating AI Summary...")

# Display sample summary
summary = """
📊 Project Status Summary (Demo)
----------------------------
• Authentication module is 80% complete
• Mobile responsiveness issues need attention
• Team is on track for the sprint goal
• 3 high-priority tasks to address
"""
print(summary)

print("✅ Demo completed successfully!")

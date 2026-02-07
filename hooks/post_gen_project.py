import os
import subprocess
import sys


def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(e)


def main():
    print("Post-generation setup starting...")

    # 1. Initialize uv and install dependencies
    try:
        # Check if uv is installed
        subprocess.check_output(["uv", "--version"])
        print("Installing dependencies with uv...")
        run_command("uv sync")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(
            "⚠️  uv is not installed. Please install it for dependency management: https://astral.sh/uv/"
        )

    # 2. Setup environment file
    if os.path.exists(".env.example"):
        os.rename(".env.example", ".env")
        print("Renamed .env.example to .env")

    print("\n✅ Project created successfully!")
    print("\nNext steps:")
    print("1. cd into the project directory")
    print("2. Run start.ps1 or start.sh to start the project")


if __name__ == "__main__":
    main()

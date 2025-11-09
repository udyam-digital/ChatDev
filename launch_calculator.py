#!/usr/bin/env python3
"""
Automated launcher for the SimpleCalc calculator application.
This script handles all dependency checks, installations, and launches the GUI.
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python 3 is installed and meets minimum requirements."""
    version = sys.version_info
    if version.major < 3:
        print("❌ Python 3 is required but Python 2 was found.")
        print("Please install Python 3 from https://www.python.org/downloads/")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_tkinter():
    """Check if Tkinter is installed and install if missing."""
    try:
        import tkinter
        print("✅ Tkinter is already installed")
        return True
    except ImportError:
        print("⚠️  Tkinter not found. Attempting to install...")
        return install_tkinter()

def install_tkinter():
    """Install Tkinter based on the operating system."""
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            print("On macOS, Tkinter should come with Python.")
            print("If you installed Python via Homebrew, try:")
            print("  brew install python-tk@3.9")
            print("\nAttempting to install via pip...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "tk"])
            
        elif system == "Linux":
            print("Attempting to install Tkinter on Linux...")
            # Try different package managers
            try:
                subprocess.check_call(["sudo", "apt-get", "install", "-y", "python3-tk"])
            except:
                try:
                    subprocess.check_call(["sudo", "yum", "install", "-y", "python3-tkinter"])
                except:
                    subprocess.check_call(["sudo", "dnf", "install", "-y", "python3-tkinter"])
                    
        elif system == "Windows":
            print("On Windows, Tkinter should come with Python.")
            print("Please reinstall Python from python.org and ensure 'tcl/tk' is selected.")
            return False
            
        # Verify installation
        import tkinter
        print("✅ Tkinter successfully installed")
        return True
        
    except Exception as e:
        print(f"❌ Failed to install Tkinter: {e}")
        print("\nManual installation required:")
        if system == "Darwin":
            print("  brew install python-tk@3.9")
        elif system == "Linux":
            print("  sudo apt-get install python3-tk")
        return False

def navigate_to_calculator_dir():
    """Navigate to the calculator directory."""
    calc_dir = os.path.expanduser("~/udyam/external/chatdev/WareHouse/SimpleCalc_DefaultOrganization_20251110004427")
    
    if not os.path.exists(calc_dir):
        print(f"❌ Calculator directory not found: {calc_dir}")
        return None
    
    print(f"✅ Found calculator directory: {calc_dir}")
    return calc_dir

def verify_main_py(calc_dir):
    """Verify that main.py exists in the calculator directory."""
    main_py_path = os.path.join(calc_dir, "main.py")
    
    if not os.path.exists(main_py_path):
        print(f"❌ main.py not found at: {main_py_path}")
        return None
    
    print(f"✅ Found main.py: {main_py_path}")
    return main_py_path

def launch_calculator(main_py_path):
    """Launch the calculator GUI."""
    print("\n🚀 Launching Simple Calculator...")
    print("=" * 60)
    
    try:
        # Change to the directory containing main.py
        calc_dir = os.path.dirname(main_py_path)
        os.chdir(calc_dir)
        
        # On macOS, set environment variable to avoid version check issues
        env = os.environ.copy()
        if platform.system() == "Darwin":
            env['TK_SILENCE_DEPRECATION'] = '1'
            # Try to use system Python's Tkinter which has proper macOS support
            system_python = subprocess.run(['which', 'python3'], 
                                         capture_output=True, 
                                         text=True).stdout.strip()
            if system_python and '/usr/bin/python3' in system_python:
                print("Using system Python for better Tkinter compatibility...")
                python_exec = system_python
            else:
                python_exec = sys.executable
        else:
            python_exec = sys.executable
        
        print(f"Executing with: {python_exec}")
        
        # Run the calculator (this will block until the window is closed)
        result = subprocess.run([python_exec, main_py_path], 
                              env=env,
                              check=True,
                              stderr=subprocess.PIPE,
                              stdout=subprocess.PIPE)
        
        if result.returncode == 0:
            print("\n✅ Calculator closed successfully")
            return True
        else:
            print(f"\n❌ Calculator exited with code: {result.returncode}")
            if result.stderr:
                print(f"Error output: {result.stderr.decode()}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running calculator: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr.decode()}")
        
        # Try alternative method: import and run directly
        print("\n🔄 Trying alternative launch method...")
        return launch_calculator_direct(main_py_path)
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def launch_calculator_direct(main_py_path):
    """Alternative method: Import and run the calculator directly."""
    try:
        print("Launching calculator by importing main.py directly...")
        
        # Add the calculator directory to the Python path
        calc_dir = os.path.dirname(main_py_path)
        sys.path.insert(0, calc_dir)
        os.chdir(calc_dir)
        
        # Import and run the main function
        import main
        main.main()
        
        print("\n✅ Calculator closed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Direct launch failed: {e}")
        return False

def main():
    """Main function to orchestrate the calculator launch."""
    print("=" * 60)
    print("🧮 Simple Calculator Launcher")
    print("=" * 60)
    print()
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        if retry_count > 0:
            print(f"\n🔄 Retry attempt {retry_count}/{max_retries}")
            print()
        
        # Step 1: Check Python version
        if not check_python_version():
            print("\n❌ Python version check failed. Exiting.")
            sys.exit(1)
        
        # Step 2: Check and install Tkinter if needed
        if not check_tkinter():
            retry_count += 1
            if retry_count < max_retries:
                print("\n⚠️  Tkinter installation failed. Retrying...")
                continue
            else:
                print("\n❌ Could not install Tkinter after multiple attempts.")
                print("Please install Tkinter manually and run this script again.")
                sys.exit(1)
        
        # Step 3: Navigate to calculator directory
        calc_dir = navigate_to_calculator_dir()
        if not calc_dir:
            print("\n❌ Cannot proceed without calculator directory.")
            sys.exit(1)
        
        # Step 4: Verify main.py exists
        main_py_path = verify_main_py(calc_dir)
        if not main_py_path:
            print("\n❌ Cannot proceed without main.py file.")
            sys.exit(1)
        
        # Step 5: Launch the calculator
        success = launch_calculator(main_py_path)
        
        if success:
            print("\n" + "=" * 60)
            print("✅ Calculator session completed successfully!")
            print("=" * 60)
            sys.exit(0)
        else:
            retry_count += 1
            if retry_count < max_retries:
                print("\n⚠️  Calculator launch failed. Retrying...")
                continue
            else:
                print("\n❌ Calculator launch failed after multiple attempts.")
                sys.exit(1)
    
    print("\n❌ Maximum retry attempts reached. Please check the errors above.")
    sys.exit(1)

if __name__ == "__main__":
    main()

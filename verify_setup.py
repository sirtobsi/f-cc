#!/usr/bin/env python
"""
Quick verification script for the FDSE Challenge repository setup.

This script checks that all components are properly configured.
Run this after initial setup or before candidate deployment.

Usage: python verify_setup.py
"""

import sys
from pathlib import Path
import subprocess


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def check_file_exists(filepath, description, required=True):
    """Check if a file exists."""
    exists = Path(filepath).exists()
    status = "✓" if exists else ("✗" if required else "⚠")
    req_text = "(required)" if required else "(optional)"
    print(f"{status} {description}: {filepath} {req_text}")
    return exists


def check_imports():
    """Check if required packages can be imported."""
    print_section("Checking Python Dependencies")
    
    packages = {
        "pandas": "pandas",
        "numpy": "numpy",
        "pytest": "pytest",
    }
    
    all_ok = True
    for name, import_name in packages.items():
        try:
            __import__(import_name)
            print(f"✓ {name} is installed")
        except ImportError:
            print(f"✗ {name} is NOT installed")
            all_ok = False
    
    return all_ok


def check_structure():
    """Check repository structure."""
    print_section("Checking Repository Structure")
    
    required_files = [
        ("README.md", "Main README"),
        ("NOTES.md", "Candidate notes template"),
        ("CONTRIBUTING.md", "Contribution guidelines"),
        ("REVIEWER_GUIDE.md", "Reviewer guide"),
        ("SETUP_GUIDE.md", "Setup guide"),
        ("requirements.txt", "Python dependencies"),
        ("pyproject.toml", "Project configuration"),
        ("src/__init__.py", "Source package"),
        ("src/data_simulator.py", "Data simulator"),
        ("src/data_processing.py", "Processing functions"),
        ("tests/test_exposed.py", "Exposed tests"),
        (".github/workflows/exposed-tests.yml", "Exposed tests workflow"),
        (".github/workflows/hidden-tests.yml", "Hidden tests workflow"),
        (".gitignore", "Git ignore file"),
        ("examples/example_usage.py", "Example usage"),
    ]
    
    optional_files = [
        ("LICENSE", "License file"),
        ("docs/index.md", "Documentation"),
    ]
    
    all_ok = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description, required=True):
            all_ok = False
    
    for filepath, description in optional_files:
        check_file_exists(filepath, description, required=False)
    
    return all_ok


def check_hidden_tests():
    """Check hidden tests setup."""
    print_section("Checking Hidden Tests")
    
    hidden_test_file = Path("tests_hidden/test_hidden.py")
    readme_file = Path("tests_hidden/README.md")
    
    readme_exists = readme_file.exists()
    test_exists = hidden_test_file.exists()
    
    if readme_exists:
        print("✓ tests_hidden/README.md exists")
    else:
        print("✗ tests_hidden/README.md missing")
    
    if test_exists:
        print("⚠ tests_hidden/test_hidden.py EXISTS in public repo")
        print("  WARNING: This file should be in a PRIVATE repository!")
        print("  See SETUP_GUIDE.md for instructions")
        return False
    else:
        print("✓ tests_hidden/test_hidden.py NOT in public repo (correct)")
    
    return readme_exists


def check_functions_not_implemented():
    """Verify that skeleton functions raise NotImplementedError."""
    print_section("Checking Function Skeletons")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from src.data_processing import ingest_data, detect_anomalies, summarize_metrics
        
        # Check that functions raise NotImplementedError
        functions = [
            ("ingest_data", ingest_data),
            ("detect_anomalies", detect_anomalies),
            ("summarize_metrics", summarize_metrics),
        ]
        
        all_ok = True
        for name, func in functions:
            try:
                # Try calling with dummy data - should raise NotImplementedError
                if name == "ingest_data":
                    func([])
                elif name == "detect_anomalies":
                    import pandas as pd
                    func(pd.DataFrame(), "test")
                else:
                    import pandas as pd
                    func(pd.DataFrame())
                print(f"⚠ {name}() does not raise NotImplementedError")
                print(f"  (This is OK if already implemented)")
            except NotImplementedError:
                print(f"✓ {name}() raises NotImplementedError (skeleton intact)")
            except Exception as e:
                if "must be implemented" in str(e):
                    print(f"✓ {name}() has proper skeleton")
                else:
                    print(f"⚠ {name}() raises: {type(e).__name__}")
                    all_ok = False
        
        return all_ok
    except Exception as e:
        print(f"✗ Error importing functions: {e}")
        return False


def check_simulator():
    """Check that the data simulator works."""
    print_section("Testing Data Simulator")
    
    try:
        from src.data_simulator import IndustrialDataSimulator
        
        sim = IndustrialDataSimulator(seed=42, dropout_rate=0.0)
        print("✓ IndustrialDataSimulator instantiated")
        
        # Try reading data
        data = sim.read_sensors(duration_seconds=5, interval_seconds=1.0)
        print(f"✓ Generated test data: {len(data)} readings")
        
        # Check expected columns
        expected_cols = ["timestamp", "sensor", "value", "unit", "quality"]
        if all(col in data.columns for col in expected_cols):
            print(f"✓ Data has expected columns: {expected_cols}")
        else:
            print(f"✗ Data missing columns. Has: {list(data.columns)}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error testing simulator: {e}")
        return False


def check_gitignore():
    """Check that .gitignore is properly configured."""
    print_section("Checking .gitignore")
    
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        print("✗ .gitignore does not exist")
        return False
    
    content = gitignore_path.read_text()
    
    required_patterns = [
        ("venv/", "Virtual environments"),
        ("__pycache__/", "Python cache"),
        (".pytest_cache/", "Pytest cache"),
        ("tests_hidden/test_hidden.py", "Hidden tests"),
    ]
    
    all_ok = True
    for pattern, description in required_patterns:
        if pattern in content:
            print(f"✓ Ignores {description}")
        else:
            print(f"⚠ Missing pattern for {description}: {pattern}")
            all_ok = False
    
    return all_ok


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("  FDSE Challenge Repository Verification")
    print("=" * 60)
    print("\nThis script verifies the repository setup.")
    print("Run from the repository root directory.")
    
    results = {
        "Structure": check_structure(),
        "Dependencies": check_imports(),
        "Function Skeletons": check_functions_not_implemented(),
        "Data Simulator": check_simulator(),
        "Hidden Tests": check_hidden_tests(),
        "Git Configuration": check_gitignore(),
    }
    
    print_section("Summary")
    
    all_passed = True
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All checks passed! Repository is ready.")
        print("\nNext steps:")
        print("1. Review SETUP_GUIDE.md for hidden tests setup")
        print("2. Configure GitHub secrets for CI/CD")
        print("3. Test with a sample candidate submission")
    else:
        print("✗ Some checks failed. Please review the output above.")
        print("\nSee SETUP_GUIDE.md for detailed setup instructions.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

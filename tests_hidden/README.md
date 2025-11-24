# Hidden Tests Directory

⚠️ **CONFIDENTIAL - Do NOT commit test files to public repository** ⚠️

This directory is for hidden tests used during final evaluation of candidate submissions.

## Setup for Reviewers

### Option 1: Clone from private repository
```bash
git clone git@github.com:Xelerit-Robotics/applicant-dojo-hidden-tests.git tests_hidden
```

### Option 2: Copy from secure location
```bash
cp -r /path/to/secure/hidden-tests/* tests_hidden/
```

## Running Hidden Tests

```bash
# From repository root
pytest tests_hidden/test_hidden.py -v --tb=short

# With detailed output
pytest tests_hidden/test_hidden.py -v --tb=long -s
```

## Security Notes

- Never commit `test_hidden.py` to the public repository
- Ensure this directory is in `.gitignore`
- Only share with authorized reviewers
- Delete after evaluation if working on shared machines

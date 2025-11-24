# FDSE Challenge Documentation

Welcome to the Forward Deployed Software Engineer (FDSE) pre-interview challenge documentation.

## For Candidates

If you're here to complete the challenge:

👉 **Start with the [README.md](../README.md)** in the repository root

This contains:
- Challenge overview and objectives
- Setup instructions
- Task descriptions
- Submission guidelines
- FAQ

## Quick Links for Candidates

- **[README.md](../README.md)** - Start here!
- **[NOTES.md](../NOTES.md)** - Template for your documentation
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Submission guidelines
- **[Example Usage](../examples/example_usage.py)** - Sample code

## For Hiring Team

Internal documentation:

- **[REVIEWER_GUIDE.md](../REVIEWER_GUIDE.md)** - How to evaluate submissions
- **[SETUP_GUIDE.md](../SETUP_GUIDE.md)** - Repository setup and maintenance

⚠️ Do not share reviewer documentation with candidates.

## Repository Structure

```
applicant-dojo/
├── src/                          # Source code
│   ├── data_simulator.py         # Industrial data simulator (DO NOT MODIFY)
│   └── data_processing.py        # Functions to implement (CANDIDATES EDIT THIS)
├── tests/                        # Exposed tests (visible to candidates)
│   └── test_exposed.py          # Public test suite
├── tests_hidden/                 # Hidden tests (private repository)
│   ├── README.md                # Setup instructions for reviewers
│   └── test_hidden.py           # Confidential test suite (not in public repo)
├── examples/                     # Example usage
│   └── example_usage.py         # Demo of complete pipeline
├── .github/                      # GitHub Actions
│   └── workflows/
│       ├── exposed-tests.yml    # Automatic testing on PR
│       └── hidden-tests.yml     # Manual evaluation trigger
├── README.md                     # Main candidate instructions
├── NOTES.md                      # Candidate documentation template
├── REVIEWER_GUIDE.md            # Evaluation guide (confidential)
├── SETUP_GUIDE.md               # Maintenance guide (confidential)
├── CONTRIBUTING.md              # Submission guidelines
└── pyproject.toml               # Project configuration
```

## The Challenge Functions

Candidates implement three functions in `src/data_processing.py`:

### 1. `ingest_data()`
Consolidate and clean multiple batches of industrial sensor data.

**Challenges:**
- Handling duplicates
- Sorting out-of-order timestamps
- Managing missing/null values
- Validating data quality

### 2. `detect_anomalies()`
Identify unusual sensor readings using statistical methods.

**Challenges:**
- Implementing z-score method (minimum requirement)
- Handling zero-variance data
- Managing edge cases (single point, all nulls)
- Meaningful anomaly scores

### 3. `summarize_metrics()`
Generate statistical summaries and data quality metrics.

**Challenges:**
- Computing robust statistics despite missing data
- Quality metric calculation
- Optional time-window aggregation
- Handling empty or single-value groups

## Data Simulator

The `IndustrialDataSimulator` intentionally creates realistic challenges:

- **Connection dropouts** (~7% failure rate)
- **Missing values** (~3% NaN readings)
- **Timestamp jitter** (readings arrive out of order)
- **Duplicates** (~0.5% of data)
- **Anomalies** (~1% unusual spikes)

This simulates real-world industrial protocols (OPC UA, Modbus).

## Testing Strategy

### Exposed Tests (Public)
Located in `tests/test_exposed.py`:
- Basic correctness checks
- Happy path validation
- Simple edge cases
- Function signature verification

Candidates can run these locally and see them in CI.

### Hidden Tests (Private)
Located in `tests_hidden/test_hidden.py` (private repository):
- Comprehensive edge cases
- Stress tests
- Production-readiness checks
- Performance validation

Only run during final evaluation to prevent gaming.

## CI/CD Pipeline

### Automatic on PR
- Runs exposed tests
- Checks code quality (black, ruff)
- Posts results to PR

### Manual Trigger
- Hiring team triggers hidden tests via GitHub Actions
- Results uploaded as artifacts
- Used for final evaluation

## Evaluation Criteria

1. **Code Quality (40%)** - Correctness, robustness, organization
2. **Problem Solving (30%)** - Edge cases, approach to uncertainty
3. **Communication (20%)** - Documentation quality, clarity
4. **Testing (10%)** - Exposed and hidden test pass rates

See [REVIEWER_GUIDE.md](../REVIEWER_GUIDE.md) for detailed rubric.

## Support

### For Candidates
- Technical questions: Open a GitHub Issue
- Logistics: careers@xelerit.com

### For Hiring Team
- Technical lead: [Configure in SETUP_GUIDE.md]
- Process questions: [Configure in SETUP_GUIDE.md]

---

**Version:** 1.0  
**Last Updated:** November 2025  
**Maintained by:** Forgis Hiring Team 
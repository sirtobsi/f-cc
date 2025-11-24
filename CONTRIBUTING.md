# Contributing Guidelines

Thank you for your interest! This repository is specifically designed as a pre-interview technical challenge for Forward Deployed Software Engineer candidates.

## 🎯 Purpose

This repository serves as:
- A standardized technical assessment for FDSE candidates
- A realistic simulation of industrial data engineering challenges
- A foundation for technical interviews

## 👥 Who Can Contribute

### Candidates
If you're completing this challenge as part of your interview process:
- **Fork** this repository to your own GitHub account
- Implement your solution in your fork
- Submit via **Pull Request** from your fork to this repository
- Do NOT modify test files or the data simulator

### Hiring Team
If you're part of the Forgis hiring team:
- See `REVIEWER_GUIDE.md` for evaluation procedures
- See `SETUP_GUIDE.md` for repository maintenance
- Contact the technical lead before making changes to core challenge components

### External Contributors
We appreciate your interest, but this repository is not accepting external contributions as it's an active hiring tool. Sharing solutions or test strategies would compromise the assessment.

## 📋 Candidate Submission Guidelines

### What to Submit

Your PR should include:
1. **Implementation** of the three core functions in `src/data_processing.py`
2. **Documentation** in `NOTES.md` explaining your approach
3. **Test results** - run `pytest tests/test_exposed.py -v` locally first

### What NOT to Change

Do not modify:
- `src/data_simulator.py` - simulates real-world data conditions
- `tests/test_exposed.py` - standardized evaluation
- Any GitHub Actions workflows
- Core configuration files (`pyproject.toml`, `requirements.txt`)

You may add helper modules or utilities if needed.

### Code Quality Expectations

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write defensive code with proper error handling
- Add comments for complex logic
- Use pandas/numpy idiomatically

### PR Template

When you open your PR, fill out the template completely:
- Test results
- Implementation summary
- Known limitations
- Time spent

## ⚠️ Important Notes

### Academic Integrity

This is an individual assessment. While you can use:
- ✅ Official documentation (pandas, numpy, Python)
- ✅ General programming resources (Stack Overflow for syntax questions)
- ✅ Your own previous work

Please do not:
- ❌ Copy solutions from others
- ❌ Share your solution publicly before hiring process completes
- ❌ Use AI tools to generate entire solutions (small queries for syntax are OK)

We value original thinking and problem-solving approach over perfect solutions.

### Questions

If you have **clarifying questions** about requirements:
- Open a GitHub Issue with the `question` label
- Email careers@xelerit.com

We cannot provide implementation help, but we're happy to clarify ambiguities in requirements.

## 🔄 Submission Process

1. **Fork** this repository
2. **Clone** your fork locally
3. **Create a branch**: `git checkout -b solution/your-name`
4. **Implement** your solution
5. **Test** locally: `pytest tests/test_exposed.py -v`
6. **Document** your approach in `NOTES.md`
7. **Commit** your changes with clear messages
8. **Push** to your fork
9. **Open a Pull Request** to this repository

Our CI will automatically run exposed tests. You'll be notified of the results.

## 🕐 Timeline

After submission:
- **Automatic**: Exposed tests run immediately
- **1-2 days**: Initial code review
- **3-5 days**: Final evaluation and decision
- **Within 1 week**: Interview invitation or feedback

## ❓ FAQ

**Q: Can I submit multiple times?**
A: You can push updates to your existing PR. We'll evaluate your most recent commit.

**Q: What if I run out of time?**
A: Submit what you have! Document in `NOTES.md` what you would do with more time. Partial quality implementations are valued.

**Q: Can I add dependencies?**
A: Stick to pandas/numpy for core functions. You can add dev dependencies (testing, linting) if needed.

**Q: How much documentation is expected?**
A: `NOTES.md` should take 15-30 minutes to complete thoughtfully. Quality over quantity.

## 📧 Contact

- **Technical questions about requirements**: Open a GitHub Issue
- **Logistics, scheduling**: careers@xelerit.com
- **Private matters**: careers@xelerit.com

---

**Good luck!** We're excited to see your approach to industrial data challenges.

*Xelerit Robotics Hiring Team*

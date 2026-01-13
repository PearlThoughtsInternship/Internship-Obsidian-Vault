# How to Contribute

## Your Contributions Matter

Every contribution to this platform advances our understanding of AI-powered code intelligence. This document explains how to contribute effectively.

---

## Contribution Types

### 1. Code Contributions

Building features for the code intelligence platform.

**Process**:
1. Check existing issues or create one describing your planned work
2. Fork the repository
3. Create a feature branch
4. Implement with tests
5. Submit PR with clear description

**Standards**:
- Follow existing code patterns
- Include tests for new functionality
- Document public APIs
- Keep PRs focused (one feature per PR)

### 2. Experiment Contributions

Running and documenting experiments on context quality.

**Process**:
1. Define hypothesis
2. Set up experiment parameters
3. Run against test questions
4. Document results in `Experiments/` folder
5. Submit findings

**Format**:
```yaml
# experiments/exp-NNN.yaml
id: "exp-NNN"
date: "YYYY-MM-DD"
contributor: "Your Name"
hypothesis: "What you're testing"

parameters:
  # Your experiment parameters

results:
  # Your measured outcomes

findings: |
  What you learned
```

### 3. Documentation Contributions

Improving platform documentation.

**Areas**:
- Product documentation (01-Product/)
- Engineering guides (02-Engineering/)
- AI Platform docs (03-AI-Platform/)
- Internship materials (04-Internship/)

**Process**:
1. Identify gap or improvement
2. Submit PR with changes
3. Follow existing documentation style

---

## Weekly Submission Process

### What to Submit

Each week, submit:

1. **Code**: Push to your fork/branch
2. **Progress Report**: Update in Contributions/Reviews/
3. **Experiment Results**: If running experiments

### Submission Format

```markdown
## Week N Update - [Your Name]

### What I Built
- [Feature/Tool description]
- [Link to PR or commit]

### What I Learned
- [Key insight 1]
- [Key insight 2]

### What Blocked Me
- [Blocker and how resolved / still open]

### Next Week
- [Planned work]
```

---

## Code Review Expectations

### For Contributors

When submitting code:
- Explain the "why" not just the "what"
- Highlight decisions you're uncertain about
- Include test evidence

### For Reviewers

When reviewing:
- Focus on correctness and clarity
- Suggest improvements constructively
- Approve when "good enough" (not perfect)

---

## Experiment Collaboration

### Sharing Findings

All experiment results should be:
- Documented in standard format
- Committed to `05-Contributions/Experiments/`
- Discussed in weekly reviews

### Building on Others' Work

When building on previous experiments:
- Reference the original experiment ID
- Explain what you're adding/changing
- Compare results explicitly

---

## Recognition

Significant contributions will be:
- Credited in documentation
- Highlighted in project updates
- Referenced for future opportunities

---

## Related

- [[Reviews/|Cohort Reviews]]
- [[Experiments/|Experiment Log]]
- [[../04-Internship/02-Week-by-Week|Weekly Schedule]]

---

*Last Updated: 2026-01-13*

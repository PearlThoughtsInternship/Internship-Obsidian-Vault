# Pull Request Template

## PR Title: [Feature/Fix/Docs]: Brief description

### 🌟 PR Information

**Date**: [[YYYY-MM-DD]]  
**Author**: [Your Name]  
**Team**: [Team Name]  
**Ticket/Task**: [Reference Number]

---

## 📝 Description

### What does this PR do?
[Provide a clear and concise description of the changes]

### Why is this change necessary?
[Explain the problem this solves or the feature it adds]

---

## 🔄 Type of Change

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🎨 Style update (formatting, missing semi-colons, etc.)
- [ ] 🔧 Code refactoring
- [ ] 🎯 Performance improvement
- [ ] ✅ Test update
- [ ] 🔐 Security fix

---

## 📋 Checklist

### Code Quality
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have removed any console.log or debugging code

### Testing
- [ ] I have tested my changes locally
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

### Documentation
- [ ] I have updated the README if needed
- [ ] I have updated API documentation if applicable
- [ ] I have added JSDoc/TSDoc comments for new functions

---

## 🧪 Implementation Details

### Files Changed
```
- src/controllers/user.controller.ts
- src/services/auth.service.ts
- tests/auth.test.ts
```

### Key Changes
1. **Change 1**: [Description]
   - File: `filename.ts`
   - Reason: [Why this change was made]

2. **Change 2**: [Description]
   - File: `filename.ts`
   - Reason: [Why this change was made]

---

## 📸 Screenshots (if applicable)

### Before
[Add screenshot or description]

### After
[Add screenshot or description]

---

## 🧪 Testing Instructions

### How to Test
1. Step 1: [Instruction]
2. Step 2: [Instruction]
3. Step 3: [Instruction]
4. Expected Result: [What should happen]

### Test Cases Covered
- ✅ Test case 1: [Description]
- ✅ Test case 2: [Description]
- ✅ Test case 3: [Description]

### API Testing (if applicable)
```bash
# Example API call
curl -X POST http://localhost:3000/api/v1/endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

---

## 🚫 Breaking Changes

### Affected Areas
- [ ] No breaking changes
- [ ] Database schema changes
- [ ] API contract changes
- [ ] Configuration changes
- [ ] Dependency updates

### Migration Steps (if applicable)
1. [Step needed to migrate]
2. [Step needed to migrate]

---

## 🔗 Related Issues/PRs

- Closes #[issue number]
- Related to #[issue/PR number]
- Depends on #[PR number]

---

## 📊 Performance Impact

### Metrics
- **Before**: [Performance metric]
- **After**: [Performance metric]
- **Improvement**: [Percentage or description]

### Considerations
- [ ] This change has no performance impact
- [ ] This change improves performance
- [ ] This change may impact performance (explain below)

---

## 🔐 Security Considerations

- [ ] No security impact
- [ ] Security improvement
- [ ] Requires security review

### Security Notes
[Any security-related information]

---

## 📄 Additional Notes

### Dependencies
- [ ] No new dependencies
- [ ] New dependencies added:
  - Package: version
  - Reason: [Why this dependency is needed]

### Known Issues
[List any known issues or limitations]

### Future Improvements
[Suggestions for future enhancements]

---

## 👥 Reviewers

### Requested Reviewers
- @mentor-name
- @team-member

### Review Checklist for Reviewers
- [ ] Code follows project conventions
- [ ] Changes are well-tested
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance impact is acceptable

---

## 📝 Mentor/Reviewer Comments

[Space for reviewer feedback]

---

### PR Status
- [ ] 🔄 Work in Progress
- [ ] 👀 Ready for Review
- [ ] ✅ Approved
- [ ] 🔧 Changes Requested
- [ ] 🎉 Merged

---

*Template Version: 1.0*
*Last Updated: [[2025-09-10]]*
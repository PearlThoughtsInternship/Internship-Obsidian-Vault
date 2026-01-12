# Pre-Internship Week Requirements

> **Timeline**: This week (7 days)
> **Goal**: Demonstrate you can follow instructions, learn independently, and produce tangible results

---

## Before You Begin: Setting Expectations

### The Reality of This Internship

We're a **small organization** with limited time and resources. We offered this internship **without any fee** because we believe in sharing knowledge and growing the next generation of engineers. But we need you to understand something important:

**Think of this like being dropped in the Amazon rainforest.**

You have:
- A compass (this documentation)
- Some basic tools (the target codebases, concepts explained here)
- Radio contact to base camp (our mentors — but we can only respond so often)

You don't have:
- A guide holding your hand through every step
- Someone doing the work for you
- Unlimited mentor time

### What This Means for You

We understand:
- **You're new to your career** — this might be your first real technical challenge
- **Remote work is hard** — no one sitting next to you to ask questions
- **The topics are complex** — DDD, AST parsing, embeddings are not simple
- **You're passionate** — you wouldn't be here otherwise

We commit to:
- **Sharing our knowledge** even during busy schedules
- **Reviewing your work** and giving feedback
- **Answering questions** when you're truly stuck (not when you haven't tried)

We expect you to:
- **Research first, ask second** — Google it, read the docs, try things
- **Show initiative** — don't wait for instructions, figure it out
- **Document your struggles** — "I tried X, Y, Z and still stuck" is a valid question
- **Produce tangible results** — something working, not just "I read the docs"

### Why This Matters

Your performance this week determines whether we continue together. We have limited mentorship capacity — we invest it in people who demonstrate they can:

1. **Survive with limited guidance** (the rainforest test)
2. **Learn independently** (we can't teach everything)
3. **Deliver results** (talk is cheap, show us)

This is not about being harsh. It's about being honest about our constraints and your opportunity.

---

## What This Week Is About

This is your **pre-internship filter week**. We're evaluating whether:

1. You can follow vague/remote instructions without hand-holding
2. You can learn new concepts independently
3. You can produce something tangible
4. You understand enough basics to justify investing 3 more weeks together

**This is NOT about perfection.** It's about demonstrating initiative, learning ability, and follow-through.

---

## Your Deliverables

By the end of this week, you must have:

### 1. Public GitHub Repository

Create a **public** repository with your work. Name it something like:
- `ai-modernization-internship`
- `legacy-code-analyzer`
- `code-intelligence-tool`

**Repository must contain:**
- [ ] Your code (whatever you build)
- [ ] A clear `README.md` explaining:
  - What you built
  - Why you made the choices you made
  - How to run it
  - What you learned
- [ ] Any generated artifacts (diagrams, extracted data, etc.)

### 2. Loom/Screencast Video (5-10 minutes)

Record yourself explaining:
- [ ] What problem you're solving
- [ ] Your understanding of the target codebase (ERPNext, Bahmni, or OpenElis)
- [ ] What your tool does
- [ ] A demo of it working
- [ ] What you learned and what was challenging

**Upload to**: Loom, YouTube (unlisted), or any video hosting. Share the link.

### 3. Written Reflection

In your README or a separate `REFLECTION.md`:
- [ ] What was your approach?
- [ ] What concepts were new to you?
- [ ] What would you do differently with more time?
- [ ] What questions do you still have?

---

## The Exercise

### Choose ONE of These Options

| Option | Target System | Focus Area | Difficulty |
|--------|--------------|------------|------------|
| **A** | ERPNext | Sales Invoice domain extraction | Medium |
| **B** | OpenElis | Lab sample workflow mapping | Medium |
| **C** | Bahmni | Clinical encounter flow | Medium-Hard |

**Recommended for beginners**: Option A (ERPNext) - richest documentation, clearest patterns.

See [[12-Project-Deep-Dives/Choosing-Your-Project|Choosing Your Project]] for detailed comparison.

---

## What You'll Build

A simple **code intelligence tool** that:

1. **Reads** source code from your chosen project
2. **Extracts** something meaningful:
   - Entity names (classes, functions, methods)
   - Relationships (who calls whom, what imports what)
   - Business rules (validation logic, calculations)
3. **Outputs** structured data:
   - JSON file with extracted entities
   - Mermaid diagram showing relationships
   - Summary document

### Minimum Viable Tool

```
INPUT:  A directory of source code (e.g., erpnext/accounts/doctype/sales_invoice/)
OUTPUT:
  - entities.json (list of classes/functions found)
  - relationships.mermaid (call graph or dependency diagram)
  - summary.md (what you found, explained)
```

### Example Output Structure

```
my-tool/
├── src/
│   └── analyzer.ts (or .py, .js)
├── output/
│   ├── entities.json
│   ├── relationships.mermaid
│   └── summary.md
├── README.md
└── REFLECTION.md
```

---

## Technical Requirements

### Language Choice

Use **whatever language you're comfortable with**:
- Python (most common, good libraries)
- TypeScript/JavaScript (good for AST parsing)
- Go (if you're adventurous)

**Recommended**: TypeScript or Python

### What Your Tool Should Do (Minimum)

1. **File Discovery**: Find all `.py`, `.java`, or `.ts` files in a directory
2. **Basic Parsing**: Extract function/class names (can use regex, doesn't need AST)
3. **Output Generation**: Create a JSON file with what you found
4. **Documentation**: Explain what you did in README

### Stretch Goals (If Time Permits)

- Use AST parsing (tree-sitter) instead of regex
- Extract call relationships (who calls whom)
- Generate Mermaid diagrams automatically
- Add semantic search with embeddings
- Build a simple CLI interface

---

## Resources to Use

### Required Reading (Do This First)

1. [[11-Understanding-Legacy-Systems/What-Is-Legacy|What Is Legacy Code?]]
2. [[11-Understanding-Legacy-Systems/Terminology-Glossary|Terminology Glossary]]
3. [[12-Project-Deep-Dives/Choosing-Your-Project|Choosing Your Project]]

### Target Codebases

Already cloned for you (or clone yourself):

```bash
# ERPNext (Python, Frappe framework)
git clone --depth 1 https://github.com/frappe/erpnext.git

# Bahmni (Java, Spring)
git clone --depth 1 https://github.com/Bahmni/bahmni-core.git

# OpenElis (Java, Lab system)
git clone --depth 1 https://github.com/Bahmni/OpenElis.git
```

### Helpful Libraries

**For Python:**
```bash
pip install tree-sitter  # AST parsing
pip install pathlib      # File handling
```

**For TypeScript:**
```bash
npm install tree-sitter tree-sitter-python tree-sitter-java
npm install glob         # File discovery
```

---

## Daily Suggested Schedule

| Day | Focus | Goal |
|-----|-------|------|
| **Day 1** | Read docs, understand problem | Mental model formation |
| **Day 2** | Choose project, explore codebase | Know your target |
| **Day 3** | Build file discovery + basic parsing | Extract entity names |
| **Day 4** | Add relationship extraction | Build call graph |
| **Day 5** | Generate outputs (JSON, Mermaid) | Tangible artifacts |
| **Day 6** | Write documentation, record Loom | Communicate your work |
| **Day 7** | Polish, submit | Final review |

---

## Submission

### Where to Submit

1. Push your code to your **public GitHub repository**
2. Share links in the #ai-internship Teams/Slack channel:
   - GitHub repo URL
   - Loom video URL

### Submission Checklist

- [ ] Public GitHub repo with code
- [ ] README.md with explanation
- [ ] REFLECTION.md with learnings
- [ ] Loom video (5-10 min)
- [ ] At least one output artifact (entities.json, diagram, etc.)

---

## Evaluation Criteria

We're looking for:

| Criteria | Weight | What We Check |
|----------|--------|---------------|
| **Follow-through** | 30% | Did you complete something? |
| **Understanding** | 25% | Does your explanation show comprehension? |
| **Code Quality** | 20% | Is your code readable and organized? |
| **Initiative** | 15% | Did you go beyond minimum requirements? |
| **Communication** | 10% | Is your documentation clear? |

**What we're NOT evaluating:**
- Perfection (bugs are okay)
- Advanced features (keep it simple)
- Prior experience (we expect you to learn)

---

## Common Questions

### "I don't know where to start"

1. Clone ERPNext
2. Open `erpnext/accounts/doctype/sales_invoice/sales_invoice.py`
3. Try to understand what it does
4. Write code to extract function names from that file
5. Expand from there

### "My code isn't working perfectly"

That's fine. Document what works, what doesn't, and why you think it's failing. Learning from failure is valuable.

### "I don't understand the target codebase"

That's the point! You're building a tool to help understand unfamiliar code. Start with small pieces, document what you learn.

### "How much time should I spend?"

Aim for 2-4 hours per day. Don't burn out. Consistent progress beats heroic effort.

### "Can I use ChatGPT/Claude to help?"

Yes, but:
1. Understand what the AI generates
2. Be able to explain it in your Loom video
3. Don't just copy-paste without comprehension

---

## Getting Help

- **Teams/Slack**: #ai-internship channel
- **Documentation**: This vault
- **Mentors**: Available for questions (don't expect hand-holding)

**Remember**: The ability to figure things out independently is what we're evaluating.

---

## Next Steps

1. Read [[11-Understanding-Legacy-Systems/What-Is-Legacy|What Is Legacy Code?]]
2. Read [[12-Project-Deep-Dives/Choosing-Your-Project|Choosing Your Project]]
3. Clone your chosen codebase
4. Start building!

---

*Good luck! Show us what you can do.*

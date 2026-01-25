# Day 10 – Import & Module Resolution

## Objective
Explain why import resolution is necessary.

## What I Built
- Import detection using AST
- Import table per file
- Call resolution using imports

## Example
Before:
invoice.validate → calculate_tax

After:
invoice.validate → tax.calculate_tax

## Limitations
- Does not yet resolve dynamic imports
- Does not handle re-exports

## Next Steps
- Cross-file symbol linking (Day 11)

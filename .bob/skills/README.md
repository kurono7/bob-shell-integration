# Bob Skills - Code Review Rules

This directory contains custom skills that guide Bob's code review and development assistance following IBM Bob's official skill structure.

## Official Bob Skill Structure

Each skill must be in its own subdirectory with a `SKILL.md` file:

```
.bob/skills/
├── README.md                           # This file
├── sql-injection-prevention/           # Skill directory
│   ├── SKILL.md                        # Main skill file (required)
│   ├── checklist.md                    # Optional: Additional checklist
│   └── examples/                       # Optional: Example files
├── solid-principles/
│   └── SKILL.md
├── security-vulnerabilities/
│   └── SKILL.md
├── architecture-patterns/
│   └── SKILL.md
└── code-quality/
    └── SKILL.md
```

## Skill File Format

Each `SKILL.md` follows this standardized structure:

```markdown
# Skill: [Skill Name]

## Description
[Clear, concise description - 2-3 sentences]

## When to Use
- [Specific scenario 1]
- [Specific scenario 2]
- [Specific scenario 3]

## Guidelines
[Detailed instructions organized in subsections]

### Subsection 1
[Specific guidance]

### Subsection 2
[Specific guidance]

## Examples

### Bad Example
```[language]
[Code showing what to avoid]
```

### Good Example
```[language]
[Code showing correct implementation]
```

## Common Pitfalls
- [Pitfall 1 and how to avoid it]
- [Pitfall 2 and how to avoid it]

## Review Checklist
- [ ] [Actionable check 1]
- [ ] [Actionable check 2]

## Severity Levels
- **Critical**: [Criteria]
- **High**: [Criteria]
- **Medium**: [Criteria]
- **Low**: [Criteria]

## Auto-fix Suggestions
[Concrete code fixes when applicable]

## Related Skills
- [Link to related skill 1]
- [Link to related skill 2]
```

## Available Skills

### Security Skills
- **sql-injection-prevention/** - Prevents SQL injection through parameterized queries (official format)
- **security-vulnerabilities/** - Comprehensive security vulnerability detection (legacy format)

### Code Quality Skills
- **solid-principles/** - SOLID principles for object-oriented design (legacy format)
- **code-quality/** - General code quality standards (legacy format)

### Architecture Skills
- **architecture-patterns/** - Software architecture patterns and best practices (legacy format)

## How Bob Loads Skills

Bob automatically discovers and loads all skills from subdirectories:

1. Scans `.bob/skills/` for subdirectories
2. Looks for `SKILL.md` in each subdirectory
3. Optionally loads supporting files in the same directory
4. Combines all skills into context for code review

### In GitHub Actions Workflows

```yaml
- name: Load Custom Skills
  run: |
    for skill_dir in .bob/skills/*/; do
      if [ -d "$skill_dir" ]; then
        skill_file="${skill_dir}SKILL.md"
        if [ -f "$skill_file" ]; then
          skill_name=$(basename "$skill_dir")
          echo "Loading: $skill_name"
          # Skill content is loaded and passed to Bob
        fi
      fi
    done
```

## Creating New Skills

### Quick Start
1. Create a new directory: `.bob/skills/my-new-skill/`
2. Create `SKILL.md` inside that directory
3. Follow the official skill structure template
4. Add supporting files if needed (optional)

### Example: Creating a New Skill

```bash
# Create skill directory
mkdir -p .bob/skills/react-hooks-best-practices

# Create main skill file
cat > .bob/skills/react-hooks-best-practices/SKILL.md << 'EOF'
# Skill: React Hooks Best Practices

## Description
Ensures React hooks are used correctly following React's rules of hooks
and best practices for performance and maintainability.

## When to Use
- When reviewing React components using hooks
- When refactoring class components to functional components
- During code reviews of React applications

## Guidelines
[... rest of skill content ...]
EOF

# Optional: Add supporting files
cat > .bob/skills/react-hooks-best-practices/checklist.md << 'EOF'
# React Hooks Review Checklist
- [ ] Hooks called at top level (not in loops/conditions)
- [ ] Custom hooks start with "use"
- [ ] Dependencies arrays are complete
EOF
```

## Supporting Files

You can add additional files alongside `SKILL.md`:

### Common Supporting Files
- `checklist.md` - Quick reference checklist
- `severity-guide.md` - Detailed severity criteria
- `examples/` - Directory with example code files
- `templates/` - Code templates or boilerplate
- `references.md` - Links to documentation

### Example with Supporting Files

```
.bob/skills/
└── sql-injection-prevention/
    ├── SKILL.md                    # Main skill (required)
    ├── checklist.md                # Quick checklist
    ├── test-cases.md               # Test inputs for validation
    └── examples/
        ├── vulnerable.py           # Bad example
        └── secure.py               # Good example
```

Bob can automatically read these files when the skill is activated.

## Skill Locations

Skills can be defined at two levels:

| Location | Scope | Use Case |
|----------|-------|----------|
| `<project>/.bob/skills/` | Project-specific | Workflows unique to this project |
| `~/.bob/skills/` | Global | Personal or organization-wide workflows |

**Priority**: If both locations contain a skill with the same name, the project-level skill takes precedence.

## Best Practices

### Naming Conventions
- Use kebab-case: `sql-injection-prevention/`
- Be descriptive: `react-hooks-best-practices/` not `react/`
- Group related skills: `security-*/`, `react-*/`

### Content Guidelines
- **Be Specific**: Use concrete metrics (e.g., "functions over 50 lines")
- **Show Examples**: Always include both good and bad code examples
- **Stay Focused**: One skill = one specific concern
- **Use Checklists**: Provide actionable review items
- **Define Severity**: Clear criteria for Critical/High/Medium/Low

### File Organization
```
my-skill/
├── SKILL.md              # Main skill (required)
├── README.md             # Optional: Skill-specific documentation
├── checklist.md          # Optional: Quick reference
├── examples/             # Optional: Example code
│   ├── bad-example.js
│   └── good-example.js
└── templates/            # Optional: Code templates
    └── template.js
```

## Severity Guidelines

### Critical
- Security vulnerabilities with immediate exploit risk
- Data loss or corruption potential
- Authentication/authorization bypass
- Production-breaking issues

### High
- Security issues requiring specific conditions
- Significant performance degradation
- Major architecture violations
- Hard-to-debug issues

### Medium
- Code quality issues affecting maintainability
- Minor performance concerns
- Inconsistent patterns
- Missing documentation

### Low
- Style inconsistencies
- Minor optimizations
- Suggestions for improvement
- Nice-to-have enhancements

## Migrating Legacy Skills

Current skills in flat file format will be migrated to the official structure:

### Migration Steps
1. Create subdirectory: `.bob/skills/skill-name/`
2. Move `skill-name.md` to `skill-name/SKILL.md`
3. Update skill content to follow official format
4. Add supporting files if needed
5. Test with Bob to ensure it loads correctly

### Migration Checklist
- [ ] Create skill subdirectory
- [ ] Rename file to `SKILL.md`
- [ ] Add "Skill:" prefix to title
- [ ] Add "Description" section (2-3 sentences)
- [ ] Add "When to Use" section (3-5 scenarios)
- [ ] Restructure "Guidelines" with clear subsections
- [ ] Ensure examples show both good and bad code
- [ ] Add "Common Pitfalls" section
- [ ] Add "Review Checklist" section
- [ ] Define "Severity Levels" clearly
- [ ] Add "Auto-fix Suggestions" where applicable
- [ ] Link "Related Skills"

## Testing Skills

Before finalizing a skill:

1. **Structure Test**: Does it follow the official format?
2. **Clarity Test**: Can Bob follow instructions without ambiguity?
3. **Example Test**: Do all code examples compile and run?
4. **Consistency Test**: Does it align with other skills?
5. **Completeness Test**: Are edge cases covered?

### Testing Locally

```bash
# Verify skill structure
ls -la .bob/skills/my-skill/SKILL.md

# Test skill loading in workflow
gh workflow run review-pr-with-skills.yml

# Check workflow logs
gh run list --workflow=review-pr-with-skills.yml
```

## Resources

### Official Documentation
- Bob Skills Guide: https://internal.bob.ibm.com/docs/ide/features/skills
- Skill Creator Guide: `../../bob-skills-global/skill-creator/SKILL.md`

### Examples
- `sql-injection-prevention/` - Example of official structure
- Legacy skills - Examples of old format (to be migrated)

## Contributing

To add a new skill:

1. Review `../../bob-skills-global/skill-creator/SKILL.md` for detailed guidelines
2. Create skill directory: `.bob/skills/my-skill/`
3. Create `SKILL.md` using the official structure
4. Add supporting files if needed
5. Test with Bob before committing
6. Update this README with the new skill

## Quality Standards

All skills must:
- Follow the official directory structure (`skill-name/SKILL.md`)
- Use clear, imperative language
- Provide actionable guidance
- Include realistic code examples
- Define severity levels
- Be focused on one specific area
- Avoid ambiguity and vague terms

## Common Mistakes to Avoid

### Wrong Structure
❌ `.bob/skills/my-skill.md` (flat file)
✅ `.bob/skills/my-skill/SKILL.md` (directory with SKILL.md)

### Too Broad
❌ `code-quality/` (covers everything)
✅ `function-length-limits/` (specific aspect)

### Missing Examples
❌ Only text descriptions
✅ Both good and bad code examples

### No Context
❌ "Don't use var"
✅ "Don't use var because it has function scope, not block scope. Use const or let."

## Support

For questions or issues with skills:

1. Check `../../bob-skills-global/skill-creator/SKILL.md` for detailed guidance
2. Review existing skills for examples
3. Test skills with Bob before deployment
4. Iterate based on Bob's behavior

---

**Note**: This directory follows IBM Bob's official skill structure. Each skill must be in its own subdirectory with a `SKILL.md` file. For creating new skills, always refer to the skill creator guide and official documentation.
# User Facts

This file is a template. Personal user information should be stored in:
`~/.mike/knowledge/personal/`

## Setup Personal Knowledge

1. Create your personal knowledge directory:
   ```bash
   mkdir -p ~/.mike/knowledge/personal
   ```

2. Add markdown/text files with information about yourself:
   - Your skills and background
   - Preferences for how Mike should respond
   - Projects you're working on
   - Any other context you want Mike to know

3. Sync to the knowledge base:
   ```bash
   mike knowledge sync --personal
   ```

## Example Personal File

Create `~/.mike/knowledge/personal/about_me.md`:
```markdown
# About Me

## Identity
- Name: Your Name
- Location: City, Country

## Professional
- Role: Your Job Title
- Skills: List your skills

## Preferences
- Communication style: Concise/Detailed
- Technical level: Beginner/Expert
```

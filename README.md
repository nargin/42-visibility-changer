# 42 Visibility Tool

Simple tool to manage visibility of your 42 School projects on GitHub.

## Features
- Finds all your 42 projects automatically
- Choose to make them private or public
- Select specific repositories or all at once
- Self-contained - no dependencies required!

## Setup

1. **Get a GitHub Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select the `repo` scope
   - Copy the generated token

2. **Set Environment Variable:**
   ```bash
   # Linux/Mac:
   export GITHUB_TOKEN=your_token_here
   
   # Windows:
   set GITHUB_TOKEN=your_token_here
   ```

## Usage

```bash
python3 42_privacy_tool_standalone.py
```

Or use the distribution package:
```bash
unzip 42-visibility-tool.zip
cd 42-visibility-tool-dist
python3 42-visibility-tool.py
```

## Example Session

```
42 Project Visibility Tool v1.0
========================================
Fetching repositories...

Found 5 42 projects:
------------------------------------------------------------

 1. libft                     public
 2. ft_printf                 public
 3. minishell-42              private
 4. philosophers              public
 5. pipex                     public

Summary: 4 public, 1 private

What would you like to do?
   1. Make repositories private
   2. Make repositories public
   3. Exit

Choose action (1/2/3): 1

Select repositories to make private:
   Available public repositories:

    1. libft                     public
    2. ft_printf                 public
    3. philosophers              public
    4. pipex                     public

Select repositories (1-4, 'all', or Enter to continue): 1 3 4

Selected: libft, philosophers, pipex

Will make these 3 repositories private:
   • libft
   • philosophers
   • pipex

Proceed with making 3 repositories private? (y/N): y

Making 3 repositories private...
   [1/3] Processing libft... Done
   [2/3] Processing philosophers... Done
   [3/3] Processing pipex... Done

Completed! 3/3 repositories made private
```

## What Projects Are Detected?

The tool automatically finds repositories that match:
- Contains "42" in the name
- Common 42 project names: libft, printf, minishell, philosophers, etc.
- Projects starting with "ft_" or "ft-"
- Piscine projects, exams, rush projects

## Requirements

- Python 3.6 or higher
- Internet connection
- GitHub account with repositories
- GitHub Personal Access Token with 'repo' scope

No additional dependencies required - uses only Python standard library!
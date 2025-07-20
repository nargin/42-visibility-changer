# 42 Visibility Tool

🎓 Manage visibility of your 42 School projects on GitHub.

## Features
- ✅ Comprehensive 42 project detection (200+ variations)
- 🎯 Make projects private 🔒 or public 🔓
- 📋 Select specific repositories or all at once
- 📦 Self-contained - no dependencies required!

## Setup
1. Get GitHub token: https://github.com/settings/tokens (select 'repo' scope)
2. Set environment: `export GITHUB_TOKEN=your_token_here`

## Usage
```bash
python3 42-visibility-tool.py
```

## Detection Coverage
Finds projects with ANY of these patterns:
- Contains "42" anywhere: `libft-42`, `42-minishell`
- Core projects: `libft`, `printf`, `minishell`, `philosophers`, etc.
- With prefixes: `ft_libft`, `ft-printf`, `42-pipex`
- Piscine: `c00`, `rush01`, `piscine-c`, `exam-rank-02`
- Specializations: `inception`, `cub3d`, `ft_transcendence`
- Common typos: `solong`, `pushswap`, `getnextline`

Over 200 variations covered!

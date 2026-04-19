# GEMINI.md

This file provides specialized guidance for Gemini CLI when working on the HiimFilter-PD2-S11 repository, specifically focusing on the Season 13 porting project.

## Primary Objective: Season 13 Porting
The current main task is porting feature-complete changes from the `season12` branch into the `season13` branch.

### Porting Workflow
1.  **Track Progress:** Always refer to `season13/season13_port_status.md` to identify the next pending commit.
2.  **Research Commits:** Use `season13/season12_commits.md` to understand the intent and scope of the Season 12 change.
3.  **Locate Segments:** Use `grep_search` within `builderfilter/` to find the correct source segments. Do NOT edit root `.filter` files.
4.  **Implement Surgically:** Apply changes to the relevant segment files, maintaining existing architectural patterns (e.g., class-specific tags `[ONLY=...]`).
5.  **Validate:** Always run `python validate_filters.py --errors-only` after making changes to ensure filter syntax is correct.
6.  **Update Status:** Mark the commit as completed `[x]` in `season13/season13_port_status.md` after successful implementation and local verification.

## Build & Local Workflow
- **Local Builds:** Use `python builderfilter/build.py` to generate filters locally for testing.
- **Vanilla Plus Focus:** During active development, the user often prefers building only the "Vanilla Plus" filter with the `Carrotizer_` prefix. Ensure `builderfilter/filters.json` reflects this preference when requested.
- **Git Hygiene:** Standard generated `Hiim*.filter` files should be ignored by `.gitignore` and kept out of the Git index. However, **`Carrotizer_Hiim*.filter` files should be tracked and NOT ignored.**

## Project Conventions
- **Aliases:** Item decorations (stars, brackets, symbols) are defined in `builderfilter/02-alias/`. Respect the style differences between `Standard`, `Hyper`, and `TalRasha`.
- **Naming:** Season 13 favors explicit names (e.g., "Small Charm") over short-hand codes (e.g., "SC") at high filter levels (FILTLVL 7+).
- **Prefixes:** Use the `Carrotizer_` prefix for personalized filter outputs as specified in `filters.json`.

## Key Reference Files
- `season13/season13_port_status.md` - The source of truth for current tasks.
- `season13/season12_commits.md` - Detailed commit log for reference.
- `builderfilter/filters.json` - Configuration for the build script.
- `validate_filters.py` - Mandatory syntax checker.

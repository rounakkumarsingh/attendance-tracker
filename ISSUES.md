# Issues

## 1. Docker Startup Interference
**Status:** Pending Verification (Fix applied)
**Description:**
On Docker startup (WSL integration), a parsing error occurred because the attendance tracker was consuming input intended for Docker's initialization scripts:
```
creating ~/.docker/run directory in Ubuntu distro: ... parsing ':exitcode=$RES" is not one of 'h', 'p', 'a', 'r', 's'.'
```
**Resolution:**
Moved the attendance check to the very end of `config.fish`, wrapped in a function that specifically checks `if status is-interactive`. This ensures all non-interactive background initializations (like Docker's) complete before the tracker starts.

## 2. WezTerm / Shell Config Loading Interruption
**Status:** Fixed
**Description:**
When the tracker was called early in the shell startup (e.g., in `conf.d`), pressing `Ctrl+C` to skip/abort it would kill the entire sourcing process, preventing subsequent configurations (aliases, themes, starship) from loading.
**Resolution:**
The tracker is now the final command executed in `config.fish`. If aborted, the shell is already fully initialized and functional.

## 3. Input Unresponsive on Shell Start
**Status:** Fixed
**Description:**
Attempts to trigger the tracker via `fish_prompt` events or early hooks resulted in the terminal input (stdin) not being correctly captured by the Python script. Users could see the prompt but could not type responses like 's'.
**Resolution:**
Refactored the logic into a dedicated function `check_daily_attendance` called as a standard foreground command at the end of `config.fish`. This ensures the terminal is fully ready for interactive input.
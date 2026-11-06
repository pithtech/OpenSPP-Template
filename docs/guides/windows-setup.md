# Windows Setup

Most participants develop on Windows. This guide covers what differs from macOS and Linux, and the errors seen most
often. The full tool installation walk-through is in `training/SETUP.md`.

## Docker Desktop with WSL 2

OpenSPP runs in Linux containers. Docker Desktop on Windows needs the **WSL 2 backend**:

1. Install Docker Desktop and accept **"Use WSL 2 instead of Hyper-V"** during setup.
2. If prompted, run `wsl --install` in an administrator PowerShell and restart.
3. In Docker Desktop **Settings > Resources**, give Docker at least **6 GB** of memory (4 GB is the minimum). A
   running OpenSPP uses about 0.5 GB; the rest is headroom for Docker itself and for a local `build`. On the WSL 2
   backend this is set in `%UserProfile%\.wslconfig`:

   ```ini
   [wsl2]
   memory=8GB
   processors=4
   ```

   Then run `wsl --shutdown` in PowerShell and restart Docker Desktop.

`.\odoo-project doctor` reports the backend and the memory it sees.

## Where to Clone

Two options. Both work; the first is faster.

| Option                                   | Speed    | How                                                                 |
| ---------------------------------------- | -------- | ------------------------------------------------------------------- |
| Inside WSL (`\\wsl$\Ubuntu\home\you\...`)| Fast     | Open an Ubuntu terminal, `git clone` there, run the CLI from there  |
| On the Windows drive (`C:\Users\you\...`)| Adequate | Clone with Git for Windows, run the CLI from PowerShell             |

Only your `dswd_*` modules are read through the bind mount; OpenSPP itself is inside the image, so the Windows-drive
option is acceptable for the training. Avoid OneDrive-synced folders: file locking breaks Docker bind mounts.

## Running the CLI

In **PowerShell** or **Command Prompt** the `.cmd` shim makes the CLI a normal command:

```powershell
.\odoo-project doctor
.\odoo-project pull
.\odoo-project start
```

`python odoo-project <command>` also works anywhere Python is on the PATH. In **Git Bash** use `./odoo-project`
as on macOS; Git Bash needs a `python3` on the PATH, which the python.org installer does not create by default, so
PowerShell is the recommended shell.

## Line Endings

`.gitattributes` forces LF on every text file and CRLF on `.cmd` files, whatever your `core.autocrlf` setting.
Nothing to configure. If a shell script inside the container ever fails with `\r: command not found`, run
`git add --renormalize .` and commit.

## Claude Code on Windows

Claude Code needs **Git for Windows** installed (it uses its bash). Install Node.js LTS, then:

```powershell
npm install -g @anthropic-ai/claude-code
claude
```

The project's post-edit lint hook is a Python script, so it runs the same on Windows as elsewhere.

## pre-commit

```powershell
pip install pre-commit
pre-commit install
```

The first run downloads the hook environments (several minutes). Node.js must be installed for the prettier and
eslint hooks.

## Common Errors

| Message                                                            | Fix                                                                                   |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| `error during connect: ... docker_engine: The system cannot find the file` | Docker Desktop is not running. Start it and wait for the whale icon to settle.        |
| `WSL 2 installation is incomplete`                                 | `wsl --update` in an administrator PowerShell, restart.                               |
| `Hardware assisted virtualization ... must be enabled`             | Enable Intel VT-x / AMD-V in the BIOS.                                                 |
| `port is already allocated` for 8069                               | `.\odoo-project stop`, or find the process with `netstat -ano \| findstr 8069`.        |
| Odoo very slow to start, or killed                                 | Raise Docker memory (see above); check `.\odoo-project doctor`.                        |
| `python : The term 'python' is not recognized`                     | Reinstall Python with **Add python.exe to PATH** ticked; open a new terminal.          |
| `unauthorized` or `denied` on `odoo-project pull`                  | Docker is not logged in to GHCR. Repeat the `docker login ghcr.io` step in `training/SETUP.md`. |
| `pull` fails for another reason                                    | No network, or the image is not published for this release. Run `.\odoo-project build`. |
| `'.' is not recognized` when running `./odoo-project`              | In PowerShell use `.\odoo-project` (backslash) or `python odoo-project`.               |

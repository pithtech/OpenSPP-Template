# Windows Setup

Most participants develop on Windows. This guide covers what differs from macOS and Linux, and the errors seen most
often. The full tool installation walk-through is in `training/SETUP.md`.

## Docker Desktop with WSL 2

OpenSPP runs in Linux containers. Docker Desktop on Windows needs the **WSL 2 backend**:

1. Install Docker Desktop and accept **"Use WSL 2 instead of Hyper-V"** during setup.
2. If prompted, run `wsl --install` in an administrator PowerShell and restart.
3. In Docker Desktop **Settings > Resources**, give Docker at least **6 GB** of memory (4 GB is the minimum). A
   running OpenSPP uses about 0.5 GB; the rest is headroom for Docker itself and for a local `build`. On the WSL 2
   backend this is set in `.wslconfig` in your user folder. In PowerShell, `notepad "$env:USERPROFILE\.wslconfig"`
   opens it (answer Yes to create it):

   ```ini
   [wsl2]
   memory=8GB
   processors=4
   ```

   Then run `wsl --shutdown` in PowerShell and restart Docker Desktop. Notepad may save the file as
   `.wslconfig.txt`, which WSL ignores: `Get-ChildItem $env:USERPROFILE\.wslconfig*` must show the name without
   `.txt`.

`.\odoo-project doctor` reports the backend and the memory it sees.

## Where to Clone

For the training, clone on the Windows drive, in your user folder: run `cd $HOME` in PowerShell, then `git clone`.
Not in Documents or Desktop, which are often synced by OneDrive: file locking breaks Docker bind mounts.

| Option                                   | Speed    | How                                                                 |
| ---------------------------------------- | -------- | ------------------------------------------------------------------- |
| On the Windows drive (`C:\Users\you\...`)| Adequate | Clone with Git for Windows, run the CLI from PowerShell. Use this for the training. |
| Inside WSL (`\\wsl$\Ubuntu\home\you\...`)| Fast     | Advanced, after the training. Needs the checklist below.            |

Only your `dswd_*` modules are read through the bind mount; OpenSPP itself is inside the image, so the Windows-drive
option is acceptable for the training.

**Auto-reload on the Windows drive.** `start --profile dev` restarts Odoo when a file changes, but file-change events
may not reach the container from `C:`. If your edits seem to have no effect, run `.\odoo-project restart` (Python
changes) or `.\odoo-project update` (XML and data changes), as on the default profile.

**Cloning inside WSL** needs all of these, in the Ubuntu terminal:

- Docker Desktop **Settings > Resources > WSL integration** turned on for the distribution.
- `python3 --version` of 3.11 or newer (Ubuntu 22.04 ships 3.10, which the CLI refuses).
- Git credentials for the private repository (Git Credential Manager from Windows, or a token).
- Its own `pre-commit`, Node.js and Claude Code.
- `docker login ghcr.io` again, unless Docker Desktop shares its credential store.

## Running the CLI

In **PowerShell** or **Command Prompt** the `.cmd` shim makes the CLI a normal command:

```powershell
.\odoo-project doctor
.\odoo-project pull
.\odoo-project start
```

In PowerShell always type the `.\` in front: a bare `odoo-project` works in Command Prompt but not in PowerShell.
`python odoo-project <command>` (or `py odoo-project <command>`) also works anywhere Python is on the PATH. In **Git
Bash** use `./odoo-project` as on macOS; Git Bash needs a `python3` on the PATH, which the python.org installer does
not create by default, so PowerShell is the recommended shell.

Windows PowerShell 5.1, the version built into Windows, has no `&&`, `||`, `/dev/null` or `grep`. Run commands one
per line, and search files with `Select-String -Path <file> -Pattern <text>` or the VS Code search.

After Ctrl+C on a command such as `.\odoo-project logs -f`, Windows asks `Terminate batch job (Y/N)?`: answer Y. It is
not an error.

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

If PowerShell says `npm.ps1 cannot be loaded because running scripts is disabled on this system` (or the same for
`claude.ps1`), allow scripts for your own account once, answering Y:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

If your laptop's policy blocks that, run `npm` and `claude` in Command Prompt (`cmd`) instead, or type `npm.cmd` and
`claude.cmd` in PowerShell.

## pre-commit

```powershell
python -m pip install pre-commit
pre-commit --version
pre-commit install
```

If `pre-commit` is not recognized, pip installed it into a Scripts folder that is not on the PATH (pip prints a
yellow warning naming the folder). Either add that folder to your PATH and open a new terminal, or use
`python -m pre_commit` wherever a guide writes `pre-commit` (for example `python -m pre_commit install`). Note that
`git commit` and `.\odoo-project lint` need `pre-commit` itself on the PATH.

The first run downloads the hook environments, including its own Node.js, from GitHub and nodejs.org (several
minutes; behind a proxy, see below).

## Corporate and Government Laptops

- **No admin rights**: Docker Desktop, `wsl --install` and the Node.js installer need an administrator. Ask IT before
  the training.
- **"You are not allowed to use Docker, you must be in the docker-users group"**: an administrator runs
  `net localgroup docker-users <your-windows-user> /add`; then sign out and back in.
- **Proxy**: set it in Docker Desktop (**Settings > Resources > Proxies**), for Git
  (`git config --global http.proxy http://proxy:port`), and as `HTTPS_PROXY` for pip, npm, pre-commit and
  `.\odoo-project vendor`. Ask IT for the address.
- **Port 8069 reserved by Windows**: `docker compose up` fails with "An attempt was made to access a socket in a way
  forbidden by its access permissions", although `doctor` says the port is available.
  `netsh int ipv4 show excludedportrange protocol=tcp` lists reserved ranges. Use `.\odoo-project start --profile dev`
  (it picks a free port and prints it), or as administrator run `net stop winnat` then `net start winnat`.
- **OneDrive**: clone in `C:\Users\<you>\` (`cd $HOME`), not in Documents or Desktop.
- **PowerShell scripts disabled**: see Claude Code on Windows above.

## Common Errors

| Message                                                            | Fix                                                                                   |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| `error during connect: ... //./pipe/dockerDesktopLinuxEngine` (or `docker_engine`): `The system cannot find the file specified` | Docker Desktop is not running. Start it and wait for the whale icon to settle.        |
| `WSL 2 installation is incomplete`                                 | `wsl --update` in an administrator PowerShell, restart.                               |
| `Hardware assisted virtualization ... must be enabled`             | Enable Intel VT-x / AMD-V in the BIOS.                                                 |
| `port is already allocated` for 8069                               | `.\odoo-project stop`, or find the process with `netstat -ano \| findstr 8069`.        |
| Odoo very slow to start, or killed                                 | Raise Docker memory (see above); check `.\odoo-project doctor`.                        |
| `python : The term 'python' is not recognized`, or `Python was not found; run without arguments to install from the Microsoft Store` | Python is not on the PATH (the second message comes from a Windows shortcut, not real Python). Reinstall Python with **Add python.exe to PATH** ticked, or turn off the `python.exe` entries in **Settings > Apps > Advanced app settings > App execution aliases**; open a new terminal. |
| `npm.ps1 cannot be loaded because running scripts is disabled`     | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, or use `npm.cmd` / Command Prompt. |
| `pre-commit : The term 'pre-commit' is not recognized`             | Add the Scripts folder pip named to the PATH, or use `python -m pre_commit`.          |
| `You are not allowed to use Docker, you must be in the docker-users group` | See Corporate and Government Laptops above.                                     |
| `An attempt was made to access a socket in a way forbidden by its access permissions` | Port 8069 is reserved by Windows; see Corporate and Government Laptops above. |
| `The token '&&' is not a valid statement separator`                | Windows PowerShell 5.1 has no `&&`; run the commands one per line.                    |
| `unauthorized` or `denied` on `odoo-project pull`                  | Docker is not logged in to GHCR. Repeat the `docker login ghcr.io` step in `training/SETUP.md`. |
| `pull` fails for another reason                                    | No network, or the image is not published for this release. Run `.\odoo-project build`. |
| `'.' is not recognized` when running `./odoo-project`              | In PowerShell use `.\odoo-project` (backslash) or `python odoo-project`.               |
| `The term 'odoo-project' is not recognized`                        | PowerShell needs the folder: type `.\odoo-project`, from the repository folder.        |
| `Terminate batch job (Y/N)?` after Ctrl+C                          | Normal for the `.cmd` shim: answer Y.                                                  |

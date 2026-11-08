# Pre-Training Setup Guide (OpenSPP Developer Training, DSWD 4Ps)

> **Author**: Edwin Gonzales **Last Updated**: November 6, 2026
>
> **Complete these steps before the training session.** Installation and downloads can take 30+ minutes depending on
> your internet speed. If you run into issues, contact your instructor ahead of time.

---

## What You Need

| Tool             | Required | Purpose                                          |
| ---------------- | -------- | ------------------------------------------------ |
| Docker Desktop   | Yes      | Runs Odoo and PostgreSQL in containers           |
| Git              | Yes      | Version control — tracks your changes            |
| Python 3.11+     | Yes      | Runs the `odoo-project` CLI and pre-commit hooks |
| Node.js 20+      | Yes      | Runs Claude Code and the pre-commit formatters   |
| pre-commit       | Yes      | Automated code quality checks on every commit    |
| Claude Code      | Yes      | AI-powered development assistant (CLI)           |
| A code editor    | Yes      | VS Code recommended (any editor works)           |
| A GitHub account | Yes      | To create your repository from the template      |

### Windows: read this first

- Use **PowerShell** for every command in this guide (Start menu, type "PowerShell").
- Installing Docker Desktop, WSL and Node.js needs **administrator rights**. If your laptop is managed by IT, ask them
  before the training.
- Windows PowerShell does not understand `&&`, `||`, `/dev/null` or `grep`. This guide gives a Windows form wherever
  that matters; type commands one per line.
- In PowerShell the project CLI is always typed with `.\` in front: `.\odoo-project doctor`, never
  `odoo-project doctor`.
- If something fails, check [Windows: If Something Blocks You](#windows-if-something-blocks-you) at the end of this
  guide and the "Common Errors" table in [docs/guides/windows-setup.md](../docs/guides/windows-setup.md#common-errors).

---

## Step 1: Install Docker Desktop

Docker Desktop includes Docker Engine, Docker Compose, and a GUI for managing containers.

### Windows

1. **Check system requirements**:

   - Windows 11, or Windows 10 22H2 with the latest updates (run `winver` to check). Docker's install page lists the
     current minimum.
   - WSL 2 enabled (Docker Desktop will prompt you to install it)
   - Hardware virtualization enabled in BIOS/UEFI (usually on by default)

2. **Download** Docker Desktop from <https://www.docker.com/products/docker-desktop/>

3. **Run the installer** — accept the defaults. When prompted:

   - Select **"Use WSL 2 instead of Hyper-V"** (recommended)
   - Check **"Add shortcut to desktop"** if you like

4. **Restart your computer** when prompted

5. **Launch Docker Desktop** — it appears in your system tray. Wait for the status to show "Docker Desktop is running"

6. **If WSL 2 is not installed**, Docker Desktop will show a link. Follow it, or run in PowerShell (as Administrator):

   ```powershell
   wsl --install
   ```

   Then restart and launch Docker Desktop again.

7. **Give Docker enough memory.** A running OpenSPP uses about 0.5 GB across its three containers, but Docker Desktop
   itself and a local image build need more: give it at least 4 GB; 6 GB or more is comfortable. In PowerShell, run
   `notepad "$env:USERPROFILE\.wslconfig"` (answer Yes to create the file) and put in:

   ```ini
   [wsl2]
   memory=8GB
   processors=4
   ```

   Save it, then run `wsl --shutdown` in PowerShell and start Docker Desktop again. (On a laptop with 8 GB of RAM use
   `memory=5GB`.) Notepad can save it as `.wslconfig.txt`, which WSL ignores:
   `Get-ChildItem $env:USERPROFILE\.wslconfig*` must show the name without `.txt`.

8. **Verify** — open a terminal (PowerShell or Command Prompt):
   ```bash
   docker --version
   docker compose version
   ```
   Both should print version numbers without errors.

> **Troubleshooting (Windows)**:
>
> - "Hardware assisted virtualization and data execution protection must be enabled in the BIOS" → Restart, enter BIOS
>   (usually F2, F12, or Del during boot), enable Intel VT-x or AMD-V
> - "WSL 2 installation is incomplete" → Run `wsl --update` in PowerShell (as Administrator)
> - Docker Desktop stuck on "Starting..." → Restart Docker Desktop, or restart your computer
> - "You are not allowed to use Docker, you must be in the 'docker-users' group" → see
>   [Windows: If Something Blocks You](#windows-if-something-blocks-you)

### macOS

1. **Download** Docker Desktop from <https://www.docker.com/products/docker-desktop/>

   - Choose **Apple Silicon** (M1/M2/M3/M4) or **Intel** based on your Mac

2. **Open the `.dmg`** and drag Docker to Applications

3. **Launch Docker Desktop** from Applications — grant permissions when prompted

4. **Wait** for the whale icon in the menu bar to show "Docker Desktop is running"

5. In **Settings > Resources** set memory to at least 6 GB

6. **Verify** — open Terminal:
   ```bash
   docker --version
   docker compose version
   ```

> **Troubleshooting (macOS)**:
>
> - "Docker Desktop requires macOS 12.0 or later" → Update macOS in System Settings → General → Software Update
> - Slow on Apple Silicon → Make sure you downloaded the Apple Silicon version, not Intel

### Linux

Docker Engine (no Desktop GUI needed):

```bash
# Ubuntu / Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose-v2

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to the docker group (avoids needing sudo)
sudo usermod -aG docker $USER
```

**Log out and log back in** for the group change to take effect.

Verify:

```bash
docker --version
docker compose version
```

> **Troubleshooting (Linux)**:
>
> - "permission denied" when running `docker` → You need to log out/in after `usermod`, or use `newgrp docker`
> - `docker compose` not found → Install `docker-compose-v2` package (not the old `docker-compose` Python package)

---

## Step 2: Install Git

### Windows

1. Download from <https://git-scm.com/download/win>
2. Run the installer — accept the defaults. The default editor for commit messages is Vim; after installing VS Code
   (Step 6) you can switch to it with `git config --global core.editor "code --wait"`.
3. Verify in a new terminal:
   ```bash
   git --version
   ```

> **Tip**: The installer includes "Git Bash", a Unix-like terminal for Windows. You can use it for the training if you
> prefer it over PowerShell.

### macOS

Git is included with the Xcode Command Line Tools:

```bash
xcode-select --install
```

Or install via Homebrew:

```bash
brew install git
```

Verify:

```bash
git --version
```

### Linux

```bash
# Ubuntu / Debian
sudo apt-get install git

# Fedora
sudo dnf install git
```

### Configure Git (all platforms)

Set your name and email (used in commit messages):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step 3: Install Python

You need Python 3.11 or later. Check if you already have it:

```bash
python --version     # Windows
python3 --version    # macOS / Linux
```

On Windows, "Python was not found; run without arguments to install from the Microsoft Store" means Python is not
installed (or not on the PATH): that message comes from a Windows shortcut, not from Python.

If not installed or below 3.11:

### Windows

1. Download from <https://www.python.org/downloads/>
2. **Important**: if the installer shows **"Add python.exe to PATH"**, check it. If python.org offers the "Python
   install manager" instead, install it, then run `py install 3.13` in a new PowerShell.
3. Verify in a new terminal:
   ```bash
   python --version
   ```

> **Note**: On Windows the command is `python` (or `py`), not `python3`. Everywhere this guide writes `python3`, use
> `python` on Windows.

### macOS

```bash
brew install python@3.12
```

Or download from <https://www.python.org/downloads/>

### Linux

```bash
# Ubuntu / Debian
sudo apt-get install python3 python3-pip python3-venv
```

---

## Step 4: Install pre-commit

pre-commit runs code quality checks automatically before each `git commit`.

Windows (PowerShell):

```powershell
python -m pip install pre-commit
```

macOS / Linux:

```bash
python3 -m pip install pre-commit
```

Verify:

```bash
pre-commit --version
```

> **Windows**: if `pre-commit` is "not recognized", pip installed it into a Scripts folder that is not on your PATH (pip
> printed a yellow warning naming that folder). Add that folder to your PATH (Start menu, "Edit environment variables
> for your account", Path, New) and open a new terminal. Until then, `python -m pre_commit --version` works.

> **Note**: After cloning your repository during the training, you'll also run `pre-commit install` inside the project
> directory to activate the hooks. This step just installs the tool itself.

---

## Step 5: Install Claude Code

Claude Code is an AI-powered CLI that helps you write, review, and debug code. It's a core part of our development
workflow.

### Install via npm (all platforms)

Claude Code requires **Node.js 20+**. Check if you have it:

```bash
node --version
```

If not installed:

- **Windows**: Download from <https://nodejs.org/> (LTS version); open a new PowerShell afterwards
- **macOS**: `brew install node`
- **Linux**: `sudo apt-get install nodejs npm` (Ubuntu/Debian) or download from <https://nodejs.org/>

Then install Claude Code globally:

```bash
npm install -g @anthropic-ai/claude-code
```

> **Windows**: if PowerShell says `npm.ps1 cannot be loaded because running scripts is disabled on this system`, run
> this once and answer `Y`, then repeat the `npm` command:
>
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```
>
> If your laptop does not allow that either, run `npm` and `claude` in **Command Prompt** (Start menu, "cmd") instead,
> or type `npm.cmd` and `claude.cmd` in PowerShell. The same applies to `claude.ps1` below.

Verify:

```bash
claude --version
```

### Configure the API Key

Your instructor will provide a shared **Anthropic API key** for the training. Set it as an environment variable so
Claude Code can authenticate.

**macOS / Linux:**

Add this line to your shell profile (`~/.zshrc`, `~/.bashrc`, or `~/.bash_profile`):

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Then reload your shell:

```bash
source ~/.zshrc    # or ~/.bashrc
```

**Windows (PowerShell):**

Set it permanently for your user:

```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
```

Then **close and reopen** your terminal for the change to take effect.

**Windows (Command Prompt):**

```cmd
setx ANTHROPIC_API_KEY "sk-ant-..."
```

Then **close and reopen** your terminal.

> **Important**: Replace `sk-ant-...` with the actual key your instructor provides. Do not share this key outside the
> training session.

To verify the key is set:

```bash
echo $ANTHROPIC_API_KEY          # macOS / Linux
echo %ANTHROPIC_API_KEY%         # Windows Command Prompt
$env:ANTHROPIC_API_KEY           # Windows PowerShell
```

You should see the key value printed (starting with `sk-ant-`).

### First-Time Setup

Run `claude` once to complete the initial setup:

```bash
claude
```

This will prompt you to:

1. **Accept the terms** — review and accept the usage terms
2. **Choose a theme** — pick your preferred terminal color scheme

Claude Code will automatically use the `ANTHROPIC_API_KEY` environment variable for authentication. Once setup is
complete, type `/exit` to leave the interactive session.

### Verify Claude Code Works

```bash
claude --version
claude "What is 2 + 2?"
```

You should see a version number and then a response from Claude.

> **Troubleshooting**:
>
> - `command not found: claude` → Make sure Node.js `bin` directory is on your PATH. Try closing and reopening your
>   terminal.
> - Windows: `claude.ps1 cannot be loaded because running scripts is disabled` → see the **Windows** note under "Install
>   via npm" above.
> - `npm ERR! EACCES` on macOS/Linux → Use `sudo npm install -g @anthropic-ai/claude-code` or fix npm permissions:
>   <https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally>
> - `Error: Invalid API key` → Verify the environment variable is set correctly (see "Configure the API Key" above).
>   Make sure you opened a **new** terminal after setting it.
> - `Error: 401 Unauthorized` → The API key may have been rotated. Ask your instructor for the current key.

---

## Step 6: Install a Code Editor

Any editor works. We recommend **Visual Studio Code**:

1. Download from <https://code.visualstudio.com/>
2. Install these extensions (optional but helpful):
   - **Python** (Microsoft) — syntax highlighting, linting
   - **XML Tools** — XML formatting and navigation

---

## Step 7: Verify Everything

Open a new terminal and run each of these, one line at a time. All should succeed:

```bash
docker --version           # Docker version 24.x or later
docker compose version     # Docker Compose version v2.x
git --version              # git version 2.x
python --version           # Python 3.11+ (macOS / Linux: python3 --version)
pre-commit --version       # pre-commit 3.x or later
claude --version           # Claude Code (any version)
```

**Expected output** (version numbers will vary):

```
Docker version 27.5.1, build 9f9e405
Docker Compose version v2.32.4
git version 2.47.1
Python 3.12.8
pre-commit 4.1.0
1.0.16 (Claude Code)
```

If any command fails, revisit the installation step for that tool.

### Final check — Docker is actually running

```bash
docker info --format "{{.ServerVersion}}"
```

It prints a version number (for example `27.5.1`) when Docker is running. If it prints an error such as
`error during connect` or `Cannot connect to the Docker daemon`, Docker is not running: launch Docker Desktop, wait for
it to finish starting, and try again.

---

## Step 8: Create Your Repository and Download the Image

Do this before the session; the downloads are large.

1. Accept the GitHub invitation to the template repository (sent by your instructor).
2. Open the template repository, <https://github.com/pithtech/OpenSPP-Template>, click **Use this template > Create a
   new repository**, choose your own account as owner, name it `dswd-4ps-modules`, keep it private, and create it.
3. **Create a token for the Docker image.** The image is private, so Docker needs to log in to GitHub once:

   1. On GitHub go to **Settings > Developer settings > Personal access tokens > Tokens (classic)** and click **Generate
      new token (classic)**.
   2. Name it `openspp-training`, set an expiry after the training, tick only **`read:packages`**, and generate it.
   3. Copy the token (it is shown once) and log Docker in. Windows PowerShell:

      ```powershell
      $env:GH_TOKEN = "<paste token>"
      $env:GH_TOKEN | docker login ghcr.io -u <your-github-username> --password-stdin
      ```

      Replace `<paste token>` and `<your-github-username>` **including the angle brackets** `< >`. If PowerShell says
      "The '<' operator is reserved for future use", a placeholder was left in.

      macOS / Linux:

      ```bash
      echo "<paste token>" | docker login ghcr.io -u <your-github-username> --password-stdin
      ```

      You should see `Login Succeeded`. Docker remembers it; you will not need the token again.

4. Clone your repository and run the first commands:

   **Windows (PowerShell):** clone into your user folder (`cd $HOME`), not into Documents, Desktop or a OneDrive folder.

   ```powershell
   cd $HOME
   git clone https://github.com/<your-account>/dswd-4ps-modules.git
   cd dswd-4ps-modules
   .\odoo-project doctor
   .\odoo-project pull
   .\odoo-project vendor
   pre-commit install
   ```

   **macOS / Linux:**

   ```bash
   git clone https://github.com/<your-account>/dswd-4ps-modules.git
   cd dswd-4ps-modules
   ./odoo-project doctor
   ./odoo-project pull
   ./odoo-project vendor
   pre-commit install
   ```

   `doctor` must show no red crosses (yellow warnings are fine at this point). `pull` downloads the OpenSPP image, about
   650 MB (2.3 GB on disk once extracted), and the PostgreSQL image. If it fails with `unauthorized` or `denied`, repeat
   the `docker login ghcr.io` step above; if it fails for another reason, run `.\odoo-project build` (macOS / Linux:
   `./odoo-project build`) instead (slower, 10 to 25 minutes). On an Apple Silicon Mac or a Windows ARM laptop, `pull`
   fails with `no matching manifest for linux/arm64`: the published image is for x86-64 (Intel or AMD) machines, so run
   `build` there.

   On Windows, if `pre-commit install` says `pre-commit` is not recognized, see Step 4. Then run the hooks once, so
   their first-time downloads (5 to 10 minutes) happen now and not during the training:

   ```bash
   pre-commit run --all-files
   ```

   If it ends with a `Failed` line, save the output and send it to your instructor; it does not stop you finishing
   step 8.

5. **Start it once and log in.** This is the finish line; everyone must reach it before the training:

   ```powershell
   .\odoo-project start
   ```

   (macOS / Linux: `./odoo-project start`. In the rest of this step, Windows commands start with `.\`, macOS and Linux
   with `./`.)

   The first start installs OpenSPP (about a minute on a fast machine, up to eight on a laptop) and ends with
   `Odoo available at: http://localhost:8069` and `Credentials: admin / admin`. Open that address, log in with `admin` /
   `admin`, and check that the page is styled: a blue menu bar on the left and **no** red "css error" banner at the
   bottom. If the page is unstyled, run `.\odoo-project doctor`, fix what it reports, and run
   `.\odoo-project resetassets`.

   Then run one module's tests, which takes a few minutes:

   ```powershell
   .\odoo-project test dswd_asset
   ```

   The summary at the end must show `Failed: 0 | Errors: 0`. If it does not, send the output to your instructor. Finally
   stop everything with `.\odoo-project stop`.

---

## What to Bring to the Training

- Your laptop with all tools installed and verified
- Your repository cloned, the image pulled, `doctor` with no red crosses, the first start done with a styled login page,
  and a passing `test dswd_asset`
- This guide for reference if anything needs troubleshooting

---

## Windows: If Something Blocks You

- **"running scripts is disabled on this system"** (`npm`, `claude`):
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer `Y`. If that is blocked too, use Command Prompt, or
  `npm.cmd` / `claude.cmd`.
- **"The term 'odoo-project' is not recognized"**: type `.\odoo-project`, from inside the `dswd-4ps-modules` folder.
- **"The token '&&' is not a valid statement separator"**: Windows PowerShell has no `&&`; run the commands one per
  line.
- **"Python was not found; run without arguments to install from the Microsoft Store"**: Python is not installed or not
  on the PATH. Redo Step 3, then open a new PowerShell.
- **`pre-commit` not recognized**: see the Windows note in Step 4.
- **No administrator rights**: Docker Desktop, WSL and Node.js need them. Ask IT, or tell your instructor before the
  training.
- **"You are not allowed to use Docker, you must be in the 'docker-users' group"**: an administrator runs
  `net localgroup docker-users <your-windows-user> /add`; then sign out and back in.
- **Behind a proxy** (downloads time out, `pull`, `vendor` or `pip` fail): set the proxy in Docker Desktop (**Settings >
  Resources > Proxies**) and ask IT for the address to use for Git, pip and npm. Details in
  [docs/guides/windows-setup.md](../docs/guides/windows-setup.md#corporate-and-government-laptops).
- **"An attempt was made to access a socket in a way forbidden by its access permissions"** on `start`: Windows has
  reserved port 8069. Run `.\odoo-project start --profile dev`, which picks a free port and prints the address.
- **Repository inside OneDrive, Documents or Desktop**: clone it again into `C:\Users\<you>\` (`cd $HOME` first).
- **Your edits seem to have no effect** with `start --profile dev`: auto-reload may not see changes on the `C:` drive.
  Run `.\odoo-project restart` (Python) or `.\odoo-project update` (XML and data).

More errors and fixes: [docs/guides/windows-setup.md, Common Errors](../docs/guides/windows-setup.md#common-errors). If
you are still stuck, run `.\odoo-project doctor *> doctor.txt` and send `doctor.txt` to your instructor.

**You're all set! See you at the training.**

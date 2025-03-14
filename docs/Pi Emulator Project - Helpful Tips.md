# Pi Emulator Project - Helpful Tips

## Pi Emulator .gitignore

It may be helpful to add filters to `.gitignore` for the image files, kernel files, test files, and any specific configuration files related to the emulator that aren't part of the main project code.

Here’s an updated `.gitignore` to exclude these additional items:

```plaintext
# Python cache and compiled files
__pycache__/
*.py[cod]

# SQLite database file
*.db

# Logs
*.log

# Virtual environment folders
venv/
.env/

# Ignore emulator and Raspberry Pi image/kernel files
*.img
kernel-qemu
bookworm_raspberry_pi_os_image.img
raspberry_pi_os_image.img

# Ignore test files
test_file.txt

# Docker and emulator setup files (adjust if necessary)
piserver/
docker-compose.yml
Dockerfile

# System or IDE-specific files
.DS_Store
.idea/
.vscode/
```

This will ignore the emulator images, kernel, and temporary test files, while keeping the main project files like `main.py`, `requirements.txt`, and `src/` directory tracked. 

After updating the `.gitignore`, you can run the following to clear out any already-staged files that should now be ignored:

```bash
git rm -r --cached .
git add .
git commit -m "Updated .gitignore and cleaned up tracked files"
``` 

This ensures that only the essential project files are included in your repository.

---

## Git-ing Content Within the Pi Emulator

You can mount the same folder to a similar path on your actual Raspberry Pi hardware, and continue using the same git repository from your Mac. This approach will keep your work synchronized across both environments, making the transition from the emulator to the actual hardware smooth.

### Steps to Proceed:

1. **Mount the Project Folder on the Raspberry Pi**:
   - You can mount your project folder on the Pi via a network file system (like NFS or SMB), or use `rsync` to sync files between your Mac and the Pi.
   - If you want a real-time synced environment, consider NFS or SSHFS to directly mount the directory on the Pi at the desired path (e.g., `/home/pi/vitaledge-pi-monitoring`).

2. **Continue Using the Same Git Repository**:
   - You can keep committing changes from your Mac, which will be reflected on the Pi if you use real-time syncing. Otherwise, push updates from your Mac to a remote repository (e.g., GitHub) and pull them onto the Pi.

3. **Update `.gitignore` for New Pi-Specific Tools**:
   - If you install Pi-specific tools or generate files unique to the hardware environment, you can add these to `.gitignore` as they arise. Some common additions might include Pi-specific config files or temporary files generated during hardware setup.

4. **Testing Pi-Specific Code**:
   - When you switch to the real Pi, make sure to test any hardware-specific code or sensor interactions, as some things might differ slightly from the emulator.

This setup will allow you to maintain a single, consistent codebase across both the emulator and the actual hardware, with minimal effort in switching environments.

---

## Common Git Status Options

To see the full tree of files with changes, including the structure of subdirectories, you can use the `git status` command with additional options or file system commands to visualize the entire directory structure:

1. **Using `git status` with `--untracked-files=all`**:
   - This will list all modified, staged, and untracked files recursively, showing you exactly what’s changed in each subdirectory.

   ```bash
   git status --untracked-files=all
   ```

2. **Using `tree` Command**:
   - If you have the `tree` command installed, you can combine it with `git status` for a visual representation of the directory structure with changes.
   
   ```bash
   git status --untracked-files=all | tree
   ```

3. **Using `git diff --name-only`**:
   - This will show a list of all files with changes, including those in subdirectories.

   ```bash
   git diff --name-only
   ```

4. **Using `find` to Show All Files in the Git Repo with Their Status**:
   - This will recursively display the directory structure and file statuses.

   ```bash
   find . -type f | git status --porcelain | less
   ```

If you don't have `tree` installed, you can add it with `brew install tree` on macOS, `sudo apt install tree` on Ubuntu, or `sudo dnf install tree` on Fedora. This can be especially helpful for a visual outline of your project directory and the modified files within it.

---

## Git Tree

To install `tree` on macOS using Homebrew, you can run the following command:

```bash
brew install tree
```

Once it’s installed, you can use `tree` to view your directory structure. For example:

```bash
tree
```

This will display the entire directory tree from the current directory. To see only the tracked changes in a Git repository, you can combine `tree` with `git status`:

```bash
git status --untracked-files=all | tree
```

Or use `tree -L 2` to limit the depth to two levels, which can be helpful for large projects.

---

To view a tree of all tracked files in a Git repository (excluding those in `.gitignore`), you can use the following commands after installing `tree`:

1. **Using `tree` with `git ls-files`**:
   This command will display a tree of only the tracked files, as `git ls-files` outputs all files tracked by Git, excluding those in `.gitignore`.

   ```bash
   tree -I "$(git ls-files --others --ignored --exclude-standard -z | xargs -0 echo | sed 's/ /|/g')"
   ```

   This command:
   - Uses `git ls-files` to get all tracked files.
   - Excludes untracked and ignored files based on `.gitignore`.

2. **Simpler Alternative**:
   If the above command is complex, another simpler approach is to output the list of tracked files and format them in a directory-like structure:

   ```bash
   git ls-files | xargs -I {} dirname {} | sort -u | xargs -I {} tree -d {}
   ```

Both commands will exclude files in `.gitignore`, giving you a view of your project’s tracked directory structure.

---

## Creating a private GitHub repository

To create a private GitHub repository named "vitaledge-pi-iot" and link it to your existing local Pi project, here are the recommended steps and best practices:

### Step 1: Create a Private Repository on GitHub

1. Go to [GitHub](https://github.com/) and log in to your account.
2. In the upper-right corner, click on the **+** icon and select **New repository**.
3. Enter the repository name: **vitaledge-pi-iot**.
4. Optionally, add a description (e.g., "IoT project for VitalEdge using Raspberry Pi").
5. Set the repository to **Private** (you can change it to public later if needed).
6. Do not initialize with a README, `.gitignore`, or license yet—your local repository already has files.
7. Click **Create repository**.

### Step 2: Link the Local Directory to the GitHub Repository

In your local terminal, navigate to the existing project directory:

```bash
cd /projects/vitaledge/pi-emulator
```

Add the new GitHub repository as a remote origin and push your existing commits:

```bash
# Add the GitHub repository as the 'origin' remote
git remote add origin https://github.com/YOUR_USERNAME/vitaledge-pi-iot.git

# Push the main branch to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 3: Organize Project Documentation

For an organized repository, create a `docs/` directory for all documentation:

1. In the project root, create the documentation folder:

   ```bash
   mkdir docs
   ```

2. Move your generated documents into the `docs/` folder:

   ```bash
   mv Vision_Document.md docs/
   mv Requirements_Document.md docs/
   mv Design_Document.md docs/
   mv API_Specification.md docs/
   mv Cookbook.md docs/
   ```

3. Keep filenames clear and concise, ensuring each document's purpose is easy to identify at a glance. Consider renaming files if necessary (e.g., `Vision_Document.md` to `Vision.md`).

### Step 4: Add a `README.md` with Key Information

In the root of your project directory, create a `README.md` with the following recommended structure:

```markdown
# VitalEdge Pi IoT Project

## Overview
This project is an IoT edge system designed for healthcare applications, running on a Raspberry Pi. It collects data from multiple sensors, performs basic analysis, and securely transmits critical health data to a backend.

## Features
- Sensor data collection and analysis on a Raspberry Pi
- Real-time transmission to a backend server
- Local database for data buffering and logging
- Edge-based alerting on critical conditions

## Project Structure
- `src/`: Source code for the Pi application, including data collection, processing, and transmission.
- `docs/`: Project documentation files, including vision, requirements, design, API specifications, and user manuals.
- `requirements.txt`: Python dependencies required for the project.
- `sensor_data.db`: Local SQLite database for storing buffered sensor data.

## Documentation
Detailed documentation is available in the `docs/` directory:
- **[Vision](docs/Vision.md)**: Project vision and objectives.
- **[Requirements](docs/Requirements.md)**: System requirements.
- **[Design](docs/Design.md)**: High-level and detailed system design.
- **[API Specification](docs/API_Specification.md)**: API endpoints and data schemas.
- **[Cookbook](docs/Cookbook.md)**: Installation and usage instructions, including setup for both emulated and physical hardware.

## Getting Started
1. **Installation**: See [Cookbook](docs/Cookbook.md) for setup and installation instructions.
2. **Running the Project**: Run `main.py` to start data collection and transmission from the Pi to the backend.
3. **Configuration**: Ensure correct backend URLs and authentication tokens are set in `src/config.py`.

## License
This project is currently private but may be made public in the future. License details will be added upon public release.
```

### Step 5: Update `.gitignore` to Exclude Sensitive/Temporary Files

In your `.gitignore`, add entries for:
- Files or directories specific to your development environment.
- Temporary or log files.
- Sensitive information.

Example entries for `.gitignore`:

```plaintext
# Logs and databases
*.log
sensor_data.db

# Emulation and build files
bookworm_raspberry_pi_os_image.img
kernel-qemu
*.img
piserver/
__pycache__/

# Python cache and virtual environments
*.pyc
*.pyo
*.pyd
*.venv/
env/
```

### Step 6: Commit and Push Changes

After updating the project structure and documentation, commit and push the changes:

```bash
git add .
git commit -m "Organize documentation and update README"
git push origin main
```

### Step 7: Verify and Update Repository Settings

- Check the repository on GitHub to confirm all files and documentation appear correctly.
- In **Settings > Manage Access**, verify access permissions.
- When ready, update **Settings > General > Make public** to share the project with others.

By following these steps, you’ll have a well-organized, documented repository with a clean structure and clear instructions, ready for future development or collaboration.

---

## Managing Pi Emulator Sessions - Exiting, Restarting, and Preparing the Environment

To manage your Pi emulator effectively, follow these steps for exiting, restarting, and preparing your environment after a reboot.

### 1. **Exiting the Pi Emulator**
   - To exit the emulator gracefully, enter `exit` in the emulator's terminal or use `Ctrl+D`.
   - If it doesn’t respond or you need to force close it, you can stop it from another terminal with:
     ```bash
     docker stop pi-emulator-instance
     ```

### 2. **Restarting the Pi Emulator**
   - To restart the emulator, rerun your Docker command. This should be similar to:
     ```bash
     docker run -it --rm --name pi-emulator-instance -v /path/to/your/local/dir:/home/pi/vitaledge-pi-monitoring pi-emulator
     ```
     Replace `/path/to/your/local/dir` with the directory you used on your Mac.

### 3. **Retaining Terminal History**
   - Docker containers do not retain terminal history by default. To keep command history:
      - Copy the history to a local file on your Mac before exiting the emulator:
        ```bash
        history > /path/to/your/local/dir/emulator_history.txt
        ```
      - After restarting, you can load the commands back into your session:
        ```bash
        source /path/to/your/local/dir/emulator_history.txt
        ```

### 4. **Restarting Key Processes after Emulator Reboot**
   - After restarting the emulator, you’ll likely need to restart some services, especially **SQLite3**.
      - Start **SQLite3** again by running:
        ```bash
        sqlite3 /home/pi/vitaledge-pi-monitoring/sensor_data.db
        ```
   - **Run Python scripts**: Restart your data collection, processing, and transmission scripts in the order your workflow specifies.

### 5. **Saving Development Work Between Sessions**
   - Make sure to commit any changes you want to keep to Git if you’re version-controlling your work.
   - Any files mounted from `/path/to/your/local/dir` will persist across sessions.

---

## Accessing Host Directories From Within the Pi Emulator

If you're unable to access your Mac folders from within the Pi emulator, the issue might be with the Docker volume mount configuration. Here’s how to ensure that your Mac folder is correctly mounted in the Pi emulator:

### Step 1: Confirm the Folder Path on Mac
   - Make sure the folder you want to mount exists on your Mac. Let’s assume the path is `/Users/your-username/projects/vitaledge/pi-emulator`.
   
### Step 2: Start the Emulator with the Correct Volume Mount
   - Use the following command to run the emulator with the volume mount option:
     ```bash
     docker run -it --rm --name pi-emulator-instance \
     -v /Users/your-username/projects/vitaledge/pi-emulator:/home/pi/vitaledge-pi-monitoring \
     pi-emulator
     ```
     - The `-v` option mounts the Mac folder on your Pi emulator at the specified path.

### Step 3: Check the Mounted Directory in the Emulator
   - After starting the container, open the terminal inside the emulator and navigate to `/home/pi/vitaledge-pi-monitoring`:
     ```bash
     cd /home/pi/vitaledge-pi-monitoring
     ls
     ```
   - You should now see the contents of your Mac folder inside the emulator.

### Step 4: Verify Docker Permissions (if mounting still doesn’t work)
   - Sometimes, Docker Desktop on macOS requires permissions to access folders. Go to **Docker Desktop** > **Settings** > **Resources** > **File Sharing**, and ensure your folder is added and has sharing permissions.
   - Restart Docker after making any changes to the file-sharing settings.

---






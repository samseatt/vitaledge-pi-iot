## Working with Pi Emulator

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

## Accessing Mac folders from within Pi emulator's linux terminal.

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
# How to make code changes on the beaglebone remotely using visual studio code

1. Install Visual Studio Code 

[Download Link](https://code.visualstudio.com/Download)

2. Open Visual Studio Code, click the extensions icon in the side panel and search for "SSH FS"

3. Install SSH FS

4. Once installed, click the settings icon in the bottom right, then "settings" in the pop up menu

5. Now, in the settings window, go to extensions, then "SSH FS Configuration"

6. Click "Edit in settings.json" in the "Sshfs: Configs" section. *Note: Not the "Sshfs: Configpaths" section

7. Change the settings.json file to:

```json
{
    "sshfs.configs": [
        {
            "root": "/home/debian/openag-device-software",
            "host": "beaglebone.local",
            "port": null,
            "username": "debian",
            "password": "openag12",
            "name": "method-pfc-bb"
        }
    ]
}
```
Then cmd+S to save

8. Go to the explorer icon in the top left

9. Select SSH file systems at the bottom of the workspace panel

10. Ensure the beaglebone is turned on then right click on "method-pfc-bb" and select "Connect as workspace folder"

This should now connect to the beaglebone and load the openag-device-software folder to your workspace. You can now make changes to the files and the changes will be written directly to the beaglebone.



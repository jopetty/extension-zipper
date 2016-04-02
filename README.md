# extension-zipper
A short python script to create a .zip archive of the current project state suitable for deployment to the Chrome Web Store

# Usage
Download ```build.py``` and place it in the root directory of your extention development folder. When you are ready to create a ZIP archive to publish to the Chrome Web Store, run ```build.py```. This will create a new archive in the ```releases/``` directory with a name of ```[NAME]_[VERSION]```, where ```[NAME]``` is the extension name and ```[VERSION]``` is the extension version as found in the extension's ```manifest.json```.

extension-zipper excludes any files listed in a ```.gitignore``` file, as well as any ```.git``` files when creating the archive.

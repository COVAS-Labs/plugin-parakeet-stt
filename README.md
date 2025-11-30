# COVAS:NEXT COVAS:NEXT Plugin Parakeet STT

Run STT locally using Nvidia Parakeet


## Features

- Feature 1
- Feature 2


## Installation

Download the latest release under the *Releases* section on the right. Follow the instructions on [COVAS:NEXT Plugins](https://ratherrude.github.io/Elite-Dangerous-AI-Integration/plugins/) to install the plugin.

Unpack the plugin into the `plugins` folder in the COVAS:NEXT AppData folder, leading to the following folder structure:
* `plugins`
    * `cn-plugin-parakett-stt`
        * `cn-plugin-parakett-stt.py`
        * `requirements.txt`
        * `deps`
        * `__init__.py`
        * etc.
    * `OtherPlugin`

# Development
During development, clone the COVAS:NEXT repository and place your plugin-project in the plugins folder.  
Install the dependencies to your local .venv virtual environment using `pip`, by running this command in the `cn-plugin-parakett-stt` folder:
```bash
  pip install -r requirements.txt
```

Follow the [COVAS:NEXT Plugin Development Guide](https://ratherrude.github.io/Elite-Dangerous-AI-Integration/plugins/Development/) for more information on developing plugins.

## Packaging
Use the `./pack.ps1` or `./pack.sh` scripts to package the plugin and any Python dependencies in the `deps` folder.

## Releasing
This project includes a GitHub Actions workflow that automatically creates releases. To create a new release:

1. Tag your commit with a version number:
   ```bash
   git tag v1.0.0
   ```
2. Push the tag to GitHub:
   ```bash
   git push origin v1.0.0
   ```

The workflow will automatically build the plugin using the pack script and create a GitHub Release with the zip file attached.
    
## Acknowledgements

 - [COVAS:NEXT](https://github.com/RatherRude/Elite-Dangerous-AI-Integration)

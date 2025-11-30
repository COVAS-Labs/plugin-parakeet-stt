# COVAS:NEXT Plugin Parakeet STT

Run STT locally using Nvidia Parakeet v3 models via Sherpa ONNX.

## About

This plugin provides offline Speech-to-Text (STT) capabilities for COVAS:NEXT using the **Nvidia Parakeet TDT** model, specifically the `sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8` quantized version. This allows for high-accuracy, low-latency transcription without requiring an internet connection or a GPU.

### Language Support
The included model is **multilingual** and supports **25 European languages**, including English, German, French, Spanish, Italian, Dutch, Polish, Russian, and more.

## Features

- **Offline Transcription**: No internet connection required.
- **High Accuracy**: Uses Nvidia's state-of-the-art Parakeet TDT architecture.
- **Efficient**: Runs on CPU using the optimized Sherpa ONNX runtime with int8 quantization.

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
 - [Sherpa ONNX](https://github.com/k2-fsa/sherpa-onnx) - For the excellent ONNX runtime wrapper.
 - [Nvidia NeMo](https://github.com/NVIDIA/NeMo) - For the Parakeet model architecture.
 - [ONNX Runtime](https://onnxruntime.ai/) - For the underlying inference engine.


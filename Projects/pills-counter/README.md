# Pills Counter / Pill Detection with YOLOv8

This project uses Ultralytics YOLOv8 to train an object-detection model on a pill-image dataset downloaded from Roboflow. The model predicts pill bounding boxes and class labels; the number of detected boxes in an image can be used as an image-level count.

The project now also includes a Streamlit interface for preparing raw images before model training or inference.

## Project files

- `yolo_training.ipynb` — notebook for downloading the dataset, training YOLOv8, validating the model, running predictions, and exporting to ONNX.
- `raw_images_processing.py` — reusable image conversion backend and CLI. Converts supported images to uniquely named JPG files; originals are preserved by default.
- `app.py` — Streamlit frontend with local-folder conversion, drag-and-drop uploads, live progress, activity logs, and downloadable logs.
- `requirements.txt` — project dependencies. Install PyTorch separately for the CPU or CUDA build that matches your machine.

## Setup

Use Python 3.10 in a virtual environment.

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install PyTorch first using the command recommended for your OS and hardware at [pytorch.org/get-started/locally](https://pytorch.org/get-started/locally/), then install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install jupyter
```

## Launch the interactive image converter

From this directory, run:

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit (normally http://localhost:8501).

### Streamlit features

- **Local folders:** convert images from a folder accessible to the computer running Streamlit.
- **Drag and drop:** upload multiple supported images through the browser.
- **Progress and logs:** see per-file success/error messages and live conversion progress; download the log after processing.
- **JPEG quality:** choose a quality value from 50 to 100 (default 95).
- **Safe originals:** originals are retained by default. Deletion is available only for local-folder conversion and occurs only after a JPG is saved successfully. Browser-uploaded originals are never deleted from your device.

Supported extensions: BMP, GIF, JPEG, JPG, PNG, TIFF, WebP and AVIF. Animated GIFs and multi-page TIFFs use the first frame/page, as with Pillow's default image opening behavior.

For hosted Streamlit deployments, local folder paths refer to the server filesystem; use the uploader to send files from your computer.

## Command-line image preprocessing

The original CLI remains supported:

```bash
python raw_images_processing.py --input-dir raw-data --output-dir data
```

To select JPEG quality:

```bash
python raw_images_processing.py --input-dir raw-data --output-dir data --quality 95
```

To explicitly delete successfully converted local originals, add `--delete-originals`. Use this option only when you have a backup.

## Roboflow dataset access

The notebook uses the Roboflow workspace/project and dataset version configured in the notebook. Set your own Roboflow API key as the `ROBOFLOW_API_KEY` environment variable before launching Jupyter. Never commit API keys.

**Windows PowerShell**
```powershell
$env:ROBOFLOW_API_KEY="YOUR_ROBOFLOW_API_KEY"
jupyter notebook
```

**macOS / Linux**
```bash
export ROBOFLOW_API_KEY="YOUR_ROBOFLOW_API_KEY"
jupyter notebook
```

## Training outputs

The notebook writes training artifacts under `runs/pill_detection/`. The best checkpoint is expected at `runs/pill_detection/weights/best.pt`. Dataset files, checkpoints, and generated predictions should remain outside Git.

## Disclaimer

This is an educational computer-vision project, not a medical device. Do not use its predictions to identify medication or make treatment decisions.

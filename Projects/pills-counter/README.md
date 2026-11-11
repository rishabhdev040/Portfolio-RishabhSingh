# Pills Counter / Pill Detection with YOLOv8

This project uses Ultralytics YOLOv8 to train an object-detection model on a pill-image dataset downloaded from Roboflow. The model predicts pill bounding boxes and class labels; the number of detected boxes in an image can be used as an image-level count.

> **Scope note:** The supplied source demonstrates image-based detection, validation, prediction, and ONNX export. It does not include a Streamlit dashboard or a real-time video counting application.

## Project files

- `yolo_training.ipynb` — cleaned notebook for downloading the dataset, training YOLOv8, validating the model, running predictions, and exporting to ONNX.
- `raw_images_processing.py` — converts supported raw images to JPG and assigns unique filenames. Original files are kept by default; deletion is opt-in.
- `requirements.txt` — Python package dependencies. Install PyTorch separately for the CPU or CUDA build that matches your machine.

## Setup

Use Python 3.10 in a virtual environment (the supplied notebook and dependency versions originate from a Python 3.10 / older YOLOv8 environment).

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

Install PyTorch first using the command recommended for your OS and hardware at [pytorch.org/get-started/locally](https://pytorch.org/get-started/locally/). Then install the project dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install jupyter
```

## Roboflow dataset access

The notebook is configured for the Roboflow workspace/project and dataset version used by the supplied notebook:

- Workspace: `seblful`
- Project: `pills-detection-s9ywn`
- Version: `19`
- Export format: `yolov8`

Set your own Roboflow API key before launching Jupyter. Do not commit API keys to Git.

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

Open `yolo_training.ipynb` and run the cells from top to bottom. The dataset is downloaded locally and is intentionally excluded from Git.

## Raw image preprocessing

Put source images in a `raw-data/` directory, then run:

```bash
python raw_images_processing.py --input-dir raw-data --output-dir data
```

The converted JPG files are written to `data/`. The original images are retained. To explicitly delete successfully converted originals, add `--delete-originals` (only do this when you have a backup).

## Training outputs

The notebook writes training artifacts under `runs/pill_detection/`. The best checkpoint is expected at:

```text
runs/pill_detection/weights/best.pt
```

Dataset files, checkpoints, and generated prediction output are ignored by this folder's `.gitignore`; keep large artifacts in an appropriate model/data store rather than committing them to this repository.

## Dataset, licensing, and attribution

The notebook downloads the Roboflow dataset listed above. Review that dataset's current license and usage terms before redistributing images or annotations. This repository does not include the dataset itself. Add any required dataset citation and attribution for third-party source material here before presenting the work publicly.

## Disclaimer

This is an educational computer-vision project, not a medical device. Do not use its predictions to identify medication or make treatment decisions.

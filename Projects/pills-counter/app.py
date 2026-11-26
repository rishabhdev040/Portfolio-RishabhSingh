from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pillow_avif  # noqa: F401 - Registers AVIF support with Pillow.
import streamlit as st
from PIL import Image, UnidentifiedImageError

from raw_images_processing import (
    SUPPORTED_SUFFIXES,
    change_format_to_jpg,
    get_unique_id,
)

st.set_page_config(page_title="Pills Counter · Image Preprocessing", page_icon="💊", layout="wide")

st.title("💊 Pills Counter")
st.caption("YOLOv8 pill-detection project · Raw image preprocessing")

st.markdown(
    """
    Convert source images into uniquely named JPEG files before using them in
    the pill-detection training and inference workflow. The existing YOLOv8
    notebook and command-line preprocessing script remain available.
    """
)

if "activity" not in st.session_state:
    st.session_state.activity = []
if "summary" not in st.session_state:
    st.session_state.summary = None

with st.sidebar:
    st.header("Conversion settings")
    quality = st.slider("JPEG quality", 50, 100, 95)
    delete_originals = st.checkbox(
        "Delete local originals after successful conversion",
        value=False,
        help="Only applies to local-folder mode. Uploaded files on your device are never deleted.",
    )
    st.caption("Supported: BMP, GIF, JPEG, PNG, TIFF, WebP and AVIF.")

local_tab, upload_tab = st.tabs(["📁 Local folders", "⬆️ Drag & drop"])

def add_log(level: str, message: str) -> None:
    icon = {"success": "🟢", "warning": "🟠", "error": "🔴", "info": "🔹"}.get(level, "•")
    st.session_state.activity.append(f"{icon} {message}")

def show_summary(converted: int, skipped: int, total: int, deleted: int = 0) -> None:
    st.session_state.summary = {
        "converted": converted, "skipped": skipped, "total": total, "deleted": deleted
    }

with local_tab:
    st.subheader("Convert a folder available to this machine")
    left, right = st.columns(2)
    with left:
        input_dir = st.text_input("Input folder", "raw-data", key="local_input")
    with right:
        output_dir = st.text_input("Output folder", "data", key="local_output")

    if st.button("Start folder conversion", type="primary", use_container_width=True):
        st.session_state.activity = []
        st.session_state.summary = None
        source = Path(input_dir).expanduser()
        destination = Path(output_dir).expanduser()
        try:
            if not source.is_dir():
                raise FileNotFoundError(f"Input directory does not exist: {source}")
            files = [
                item for item in source.iterdir()
                if item.is_file() and item.suffix.lower() in SUPPORTED_SUFFIXES
            ]
            if not files:
                st.warning("No supported images found in the input folder.")
            else:
                progress = st.progress(0, text="Starting…")
                status = st.empty()
                def on_progress(done: int, total: int, filename: str) -> None:
                    progress.progress(done / total, text=f"{done}/{total} · {filename}")
                    status.caption(f"Processed {done} of {total} files")
                def on_log(level: str, message: str) -> None:
                    add_log(level, message)

                converted = change_format_to_jpg(
                    source,
                    destination,
                    delete_originals=delete_originals,
                    quality=quality,
                    progress_callback=on_progress,
                    log_callback=on_log,
                )
                skipped = len(files) - converted
                deleted = converted if delete_originals else 0
                show_summary(converted, skipped, len(files), deleted)
                st.success(f"Folder conversion complete: {converted} JPG file(s) created.")
        except Exception as exc:
            add_log("error", str(exc))
            st.error(str(exc))

with upload_tab:
    st.subheader("Drop images or browse to upload")
    st.info(
        "Uploads are processed by the machine running Streamlit. The originals on your "
        "computer are never deleted, even if the deletion option is enabled."
    )
    uploads = st.file_uploader(
        "Choose image files",
        type=["bmp", "gif", "jpeg", "jpg", "png", "tif", "tiff", "webp", "avif"],
        accept_multiple_files=True,
    )
    output_dir_upload = st.text_input("Output folder on Streamlit host", "data", key="upload_output")

    if uploads:
        st.write(f"{len(uploads)} file(s) selected")
        cols = st.columns(5)
        for index, uploaded in enumerate(uploads[:10]):
            try:
                with Image.open(BytesIO(uploaded.getvalue())) as preview:
                    cols[index % 5].image(preview.copy(), caption=uploaded.name, use_container_width=True)
            except (OSError, UnidentifiedImageError):
                cols[index % 5].caption(uploaded.name)

    if st.button("Convert uploaded images", type="primary", use_container_width=True, disabled=not uploads):
        st.session_state.activity = []
        st.session_state.summary = None
        destination = Path(output_dir_upload).expanduser()
        destination.mkdir(parents=True, exist_ok=True)
        ids = get_unique_id()
        progress = st.progress(0, text="Starting…")
        converted = skipped = 0
        for index, uploaded in enumerate(uploads, start=1):
            name = Path(uploaded.name).name
            try:
                if Path(name).suffix.lower() not in SUPPORTED_SUFFIXES:
                    raise ValueError("Unsupported image format")
                with Image.open(BytesIO(uploaded.getvalue())) as image:
                    jpg = image.convert("RGB")
                    while True:
                        target = destination / f"{next(ids)}.jpg"
                        if not target.exists():
                            break
                    jpg.save(target, format="JPEG", quality=quality)
                converted += 1
                add_log("success", f"Saved: {target.name} ← {name}")
            except (OSError, UnidentifiedImageError, ValueError) as exc:
                skipped += 1
                add_log("error", f"Skipped {name}: {exc}")
            progress.progress(index / len(uploads), text=f"{index}/{len(uploads)} · {name}")
        show_summary(converted, skipped, len(uploads))
        st.success(f"Upload conversion complete: {converted} JPG file(s) created.")

st.divider()
st.subheader("Conversion summary")
if st.session_state.summary:
    values = st.session_state.summary
    a, b, c, d = st.columns(4)
    a.metric("Converted", values["converted"])
    b.metric("Skipped", values["skipped"])
    c.metric("Processed", values["total"])
    d.metric("Originals deleted", values["deleted"])
else:
    st.caption("Summary appears here after a conversion run.")

st.subheader("Activity log")
if st.session_state.activity:
    log_text = "\n".join(st.session_state.activity)
    st.code(log_text, language="text")
    st.download_button("Download log", log_text, file_name="pills-counter-image-log.txt", mime="text/plain")
else:
    st.caption("No conversion activity yet.")

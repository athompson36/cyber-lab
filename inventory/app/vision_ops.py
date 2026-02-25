"""
Workspace vision: object detection (YOLOv8) and overlay drawing.
Used by the Workspace tab for AI overlay and object detection.
"""
from __future__ import annotations

import threading
from typing import Any

# Lazy-loaded model; cache on first use
_yolo_model: Any = None
_yolo_lock = threading.Lock()


def run_detection(frame_bgr) -> list[dict[str, Any]]:
    """
    Run YOLOv8 on a BGR frame (numpy array). Returns list of detections:
    [{ "class": str, "confidence": float, "bbox": [x1, y1, x2, y2] }, ...].
    Uses yolov8n (nano) on CPU. Lazy-loads model; returns [] if ultralytics/opencv missing.
    """
    try:
        import cv2
    except ImportError:
        return []

    if frame_bgr is None or not hasattr(frame_bgr, "shape"):
        return []

    global _yolo_model
    with _yolo_lock:
        if _yolo_model is None:
            try:
                from ultralytics import YOLO
                _yolo_model = YOLO("yolov8n.pt")
            except ImportError:
                return []

    try:
        results = _yolo_model(frame_bgr, verbose=False)
    except Exception:
        return []

    out = []
    for r in results:
        if r.boxes is None:
            continue
        boxes = r.boxes
        names = r.names or {}
        for i in range(len(boxes)):
            xyxy = boxes.xyxy[i]
            conf = float(boxes.conf[i]) if boxes.conf is not None else 0.0
            cls_id = int(boxes.cls[i]) if boxes.cls is not None else 0
            class_name = names.get(cls_id, "unknown")
            out.append({
                "class": class_name,
                "confidence": round(conf, 3),
                "bbox": [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])],
            })
    return out

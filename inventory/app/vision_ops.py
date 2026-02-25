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


def draw_overlay(
    frame_bgr,
    detections: list[dict[str, Any]],
    current_step_index: int | None = None,
    focus_keyword: str | None = None,
):
    """
    Draw bounding boxes and class labels on frame_bgr (in-place).
    If focus_keyword is set, draw matching detection(s) with distinct color/thickness.
    Returns the same frame (modified).
    """
    try:
        import cv2
    except ImportError:
        return frame_bgr

    if frame_bgr is None or not detections:
        return frame_bgr

    for d in detections:
        bbox = d.get("bbox")
        if not bbox or len(bbox) != 4:
            continue
        x1, y1, x2, y2 = bbox
        class_name = d.get("class", "?")
        conf = d.get("confidence", 0)
        label = f"{class_name} {conf:.2f}"

        # Emphasize if this detection matches the current step's focus
        is_focus = (
            focus_keyword
            and focus_keyword.lower() in (class_name or "").lower()
        )
        if is_focus:
            color = (0, 255, 0)  # green
            thickness = 3
        else:
            color = (0, 165, 255)  # orange
            thickness = 2

        cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color, thickness)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(frame_bgr, (x1, y1 - th - 6), (x1 + tw, y1), color, -1)
        cv2.putText(
            frame_bgr, label, (x1, y1 - 4),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
        )

    return frame_bgr

"""
Workspace vision: object detection (YOLOv8) and overlay drawing.
Used by the Workspace tab for AI overlay and object detection.
Filters out the workstation mat (large surface) so only objects on top are reported.
Supports segmentation (yolov8n-seg) for irregular shapes; falls back to box-only.
"""
from __future__ import annotations

import threading
from typing import Any

import cv2
import numpy as np

# Lazy-loaded model; cache on first use. _yolo_has_seg True when seg model loaded.
_yolo_model: Any = None
_yolo_has_seg = False
_yolo_lock = threading.Lock()

# Robustness: ignore detections that are likely the workstation mat or background
MIN_CONFIDENCE = 0.25
MAX_BBOX_AREA_FRACTION = 0.35  # Detections covering >35% of frame are treated as mat/desk surface
IGNORE_CLASSES = frozenset({
    "dining table", "bed", "couch", "potted plant",
    "tv", "monitor", "laptop",  # often part of the scene, not "on the mat"
})


def _filter_detections(
    detections: list[dict[str, Any]],
    frame_height: int,
    frame_width: int,
) -> list[dict[str, Any]]:
    """Keep only detections that are likely objects ON the mat (not the mat itself)."""
    if not detections or frame_height <= 0 or frame_width <= 0:
        return detections
    area_total = frame_height * frame_width
    out = []
    for d in detections:
        if d.get("confidence", 0) < MIN_CONFIDENCE:
            continue
        class_name = (d.get("class") or "").strip().lower()
        if class_name in IGNORE_CLASSES:
            continue
        bbox = d.get("bbox")
        if not bbox or len(bbox) != 4:
            continue
        x1, y1, x2, y2 = bbox
        contour = d.get("contour")
        if contour and len(contour) >= 3:
            area = float(cv2.contourArea(np.array(contour, dtype=np.int32)))
        else:
            w = max(0, x2 - x1)
            h = max(0, y2 - y1)
            area = w * h
        if area_total > 0 and (area / area_total) > MAX_BBOX_AREA_FRACTION:
            continue  # too large = likely mat/desk surface
        out.append(d)
    return out


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

    global _yolo_model, _yolo_has_seg
    with _yolo_lock:
        if _yolo_model is None:
            try:
                from ultralytics import YOLO
                _yolo_model = YOLO("yolov8n-seg.pt")
                _yolo_has_seg = True
            except Exception:
                try:
                    _yolo_model = YOLO("yolov8n.pt")
                    _yolo_has_seg = False
                except Exception:
                    _yolo_model = None
                    return []

    if _yolo_model is None:
        return []

    try:
        results = _yolo_model(frame_bgr, verbose=False)
    except Exception:
        return []

    h, w = frame_bgr.shape[:2]
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
            det = {
                "class": class_name,
                "confidence": round(conf, 3),
                "bbox": [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])],
            }
            if _yolo_has_seg and r.masks is not None and hasattr(r.masks, "xy") and i < len(r.masks.xy):
                xy = r.masks.xy[i]
                if xy is not None and hasattr(xy, "__len__") and len(xy) >= 3:
                    pts = np.asarray(xy, dtype=np.int32)
                    pts[:, 0] = np.clip(pts[:, 0], 0, w - 1)
                    pts[:, 1] = np.clip(pts[:, 1], 0, h - 1)
                    det["contour"] = pts.tolist()
            out.append(det)
    return _filter_detections(out, h, w)


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

        contour = d.get("contour")
        if contour and len(contour) >= 3:
            pts = np.array(contour, dtype=np.int32)
            cv2.polylines(frame_bgr, [pts], True, color, thickness)
        else:
            cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color, thickness)

        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(frame_bgr, (x1, y1 - th - 6), (x1 + tw, y1), color, -1)
        cv2.putText(
            frame_bgr, label, (x1, y1 - 4),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
        )

    return frame_bgr

# Workspace Segmentation Masks Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add pixel-level mask/contour output to Workspace detection (YOLOv8-seg) and draw irregular shapes on the overlay, with bbox fallback when masks are missing.

**Architecture:** Replace detection model with yolov8n-seg.pt (fallback to yolov8n.pt if seg fails). Extract contours from result.masks.xy per detection; filter by contour area when present; draw contour (outline + optional fill) in overlay, else rectangle.

**Tech Stack:** Ultralytics YOLOv8 (seg), OpenCV (contours, drawContours/fillPoly), existing Flask stream and vision_ops.

---

## Task 1: Load seg model with fallback and expose model type

**Files:**
- Modify: `inventory/app/vision_ops.py` (model load block and add a flag or keep opaque)

**Step 1: Add seg model load with fallback**

In `vision_ops.py`, replace the model load block (lines ~69–75) so we try `yolov8n-seg.pt` first, then `yolov8n.pt`. Use a module-level variable `_yolo_has_seg` (bool) set to True only when seg loads, so `run_detection` and filtering/drawing know whether to use masks.

```python
# At top with other globals, add:
_yolo_has_seg = False

# In the model load block (inside _yolo_lock), replace with:
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
# Then in run_detection, only iterate r.masks if _yolo_has_seg and r.masks is not None.
```

**Step 2: Verify**

Run the app (or a one-off script that imports vision_ops and calls run_detection on a small numpy array). First run will download yolov8n-seg.pt; if that fails, box-only model should load. No automated test required for this task if no test harness exists; manual smoke test after Task 2 is acceptable.

**Step 3: Commit**

```bash
git add inventory/app/vision_ops.py
git commit -m "feat(vision_ops): load yolov8n-seg with fallback to box-only"
```

---

## Task 2: Extract contours from seg results and add to detection dict

**Files:**
- Modify: `inventory/app/vision_ops.py` (run_detection loop)

**Step 1: In run_detection, after building each detection dict, add contour when seg and masks exist**

For each detection index `i`: if `_yolo_has_seg` and `r.masks` is not None and `i < len(r.masks)`, get polygon from `r.masks.xy[i]` (Ultralytics returns list of segments; `masks.xy[i]` is the polygon for the i-th detection). Convert to list of integer pairs and append as `"contour": [[x1,y1], [x2,y2], ...]` to the detection dict. Clip coordinates to frame bounds (0, 0, w, h). If polygon has fewer than 3 points, omit contour.

Reference: Ultralytics `results[0].masks.xy` is a list of arrays, one per detection; each array is (N, 2) in pixel coords.

```python
# Inside the for i in range(len(boxes)) loop, after appending the base dict:
det = {
    "class": class_name,
    "confidence": round(conf, 3),
    "bbox": [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])],
}
if _yolo_has_seg and r.masks is not None and i < len(r.masks.xy):
    xy = r.masks.xy[i]  # numpy (N,2) or list
    if xy is not None and hasattr(xy, '__len__') and len(xy) >= 3:
        import numpy as np
        pts = np.asarray(xy, dtype=np.int32)
        pts[:, 0] = np.clip(pts[:, 0], 0, w - 1)
        pts[:, 1] = np.clip(pts[:, 1], 0, h - 1)
        det["contour"] = pts.tolist()
out.append(det)
```

**Step 2: Verify**

Run detection on a frame; inspect one detection that has a mask (e.g. cell phone). Assert `"contour" in det` and `len(det["contour"]) >= 3`.

**Step 3: Commit**

```bash
git add inventory/app/vision_ops.py
git commit -m "feat(vision_ops): add contour from seg masks to detection dict"
```

---

## Task 3: Filter by contour area when present

**Files:**
- Modify: `inventory/app/vision_ops.py` (_filter_detections)

**Step 1: Use contour area in _filter_detections when contour is present**

In `_filter_detections`, for each detection: if `d.get("contour")` exists and has at least 3 points, compute area with `cv2.contourArea(np.array(d["contour"], dtype=np.int32))`. Use that area for the MAX_BBOX_AREA_FRACTION check instead of bbox area. Otherwise keep current bbox-area logic.

```python
# Replace the bbox area block with:
bbox = d.get("bbox")
if not bbox or len(bbox) != 4:
    continue
x1, y1, x2, y2 = bbox
contour = d.get("contour")
if contour and len(contour) >= 3:
    import numpy as np
    area = cv2.contourArea(np.array(contour, dtype=np.int32))
else:
    w = max(0, x2 - x1)
    h = max(0, y2 - y1)
    area = w * h
if area_total > 0 and (area / area_total) > MAX_BBOX_AREA_FRACTION:
    continue
out.append(d)
```

Add `import numpy as np` at top of file if not present; use cv2.contourArea (cv2 already imported in run_detection; _filter_detections doesn't use cv2 today—so we need to import cv2 at the top of vision_ops or inside _filter_detections for contourArea). Prefer top-level `import cv2` in vision_ops for consistency.

**Step 2: Verify**

Unit test or manual: pass detections with contour covering 40% of frame; they should be filtered out. With contour covering 10%, kept.

**Step 3: Commit**

```bash
git add inventory/app/vision_ops.py
git commit -m "feat(vision_ops): filter by contour area when present"
```

---

## Task 4: Draw contour or bbox in overlay

**Files:**
- Modify: `inventory/app/vision_ops.py` (draw_overlay)

**Step 1: In draw_overlay, for each detection: if contour present, draw contour (fillPoly + polylines), else draw rectangle**

Use same color/thickness/focus logic as today. Label stays at bbox top-left (x1, y1). For contour: `cv2.fillPoly(frame_bgr, [pts], color)` with slight alpha if desired (optional); then `cv2.polylines(frame_bgr, [pts], True, color, thickness)`. Convert contour list to numpy array with dtype=np.int32 for OpenCV.

```python
for d in detections:
    bbox = d.get("bbox")
    if not bbox or len(bbox) != 4:
        continue
    x1, y1, x2, y2 = bbox
    class_name = d.get("class", "?")
    conf = d.get("confidence", 0)
    label = f"{class_name} {conf:.2f}"
    is_focus = (
        focus_keyword
        and focus_keyword.lower() in (class_name or "").lower()
    )
    if is_focus:
        color = (0, 255, 0)
        thickness = 3
    else:
        color = (0, 165, 255)
        thickness = 2

    contour = d.get("contour")
    if contour and len(contour) >= 3:
        import numpy as np
        pts = np.array(contour, dtype=np.int32)
        cv2.fillPoly(frame_bgr, [pts], color)  # optional: blend for alpha
        cv2.polylines(frame_bgr, [pts], True, color, thickness)
    else:
        cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color, thickness)

    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(frame_bgr, (x1, y1 - th - 6), (x1 + tw, y1), color, -1)
    cv2.putText(frame_bgr, label, (x1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
```

**Step 2: Verify**

Load Workspace tab with overlay on; confirm irregular shapes drawn for masked objects and boxes for others.

**Step 3: Commit**

```bash
git add inventory/app/vision_ops.py
git commit -m "feat(vision_ops): draw contour overlay when present, else bbox"
```

---

## Task 5: Serialize contour for API (optional)

**Files:**
- Check: `inventory/app/app.py` (api_workspace_detections and any JSON response using detections)

**Step 1: Ensure contour is JSON-serializable**

Detection dicts are returned by `GET /api/workspace/detections`. Contour is already a list of lists ([[x,y],...]); no change needed unless numpy arrays were stored. If we stored numpy in the list, convert to list in run_detection (we did .tolist() in Task 2). Verify: `curl http://localhost:5050/api/workspace/detections` returns valid JSON with detections[].contour when present.

**Step 2: Commit** (if any fix)

```bash
git add inventory/app/vision_ops.py
git commit -m "fix: ensure contour is JSON-serializable in detections"
```

---

## Task 6: Update design doc status and deploy note

**Files:**
- Modify: `docs/plans/2026-02-26-workspace-segmentation-masks-design.md` (Status line)

**Step 1: Set status to Implemented**

Change first line from `**Status:** Draft for approval` to `**Status:** Implemented (2026-02-26)`.

**Step 2: Optional PROJECT_STRUCTURE**

If PROJECT_STRUCTURE.md has a "Workspace" or "Detection" subsection, add one line: "Object detection uses YOLOv8n-seg (masks/contours) with fallback to box-only."

**Step 3: Commit**

```bash
git add docs/plans/2026-02-26-workspace-segmentation-masks-design.md
git commit -m "docs: mark segmentation masks design as implemented"
```

---

## Execution Handoff

Plan complete and saved to `docs/plans/2026-02-26-workspace-segmentation-masks-implementation.md`.

**Two execution options:**

1. **Subagent-Driven (this session)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Parallel Session (separate)** — Open a new session with executing-plans, batch execution with checkpoints.

**Which approach?**

If you prefer to have me implement it directly in this session without subagents, say "implement it here" and I’ll execute the tasks in order.

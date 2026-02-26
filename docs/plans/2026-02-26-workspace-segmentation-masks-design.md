# Workspace Detection: Irregular Shapes & Mask Overlay — Design

**Status:** Implemented (2026-02-26)  
**Date:** 2026-02-26

---

## 1. Goal

Enhance the Workspace detection layer to output **pixel-level shapes** (masks or contours) for objects, not just bounding boxes. Overlay should draw these irregular regions. All runs on **CPU on fs-dev** (same container, no new infra). This improves visibility for odd-shaped items (boards, cables, tools) and sets the base for future “deeper” AI (e.g. GPU or second-stage models) without changing the pipeline contract.

---

## 2. Approach Chosen

**Single-model segmentation (YOLOv8-seg, nano), CPU-only.**

- Replace `yolov8n.pt` with **`yolov8n-seg.pt`** in the same Flask/vision_ops pipeline.
- Detection output is extended: each item keeps `class`, `confidence`, `bbox`; add optional **`contour`** (list of `[x,y]` points) or **`mask`** (raster) when the seg model provides a mask.
- Filtering (mat/surface, ignore list, confidence) applies to **mask area when present, else bbox area**.
- Overlay: **draw contour** (or filled semi-transparent mask) when contour/mask is available; **fallback to bbox** when not (so every detection still shows something).

**Alternatives considered:**

- **Two-stage (detect then seg on crops):** More flexible but two models and slower on CPU; rejected for “A”.
- **Box-only + polygon post-process:** No standard lightweight path; rejected.

---

## 3. Data Contract

**Detection item (unchanged for consumers that only use bbox):**

- `class` (str), `confidence` (float), `bbox` (list of 4 ints) — always.
- **New, optional:** `contour` — list of `[x, y]` points (integer) forming a closed polygon; or `mask` — 2D numpy array (H×W) or shape/size metadata if we store raster. Prefer **contour** for smaller payloads and simpler drawing (cv2.polylines / fillPoly).

**API:** `GET /api/workspace/detections` continues to return `{ "detections": [ ... ] }`. Existing clients that ignore contour still work. Overlay and chat use contour when present.

---

## 4. Pipeline Changes

| Step | Current | New |
|------|--------|-----|
| Model load | `YOLO("yolov8n.pt")` | `YOLO("yolov8n-seg.pt")` |
| Inference | `model(frame)` → boxes | same; result has `results[0].masks` |
| Per-detection | bbox, class, conf | bbox, class, conf, **contour** (from mask) |
| Filter | bbox area vs frame | **mask area** (if contour/mask) else bbox area vs frame |
| Overlay | rectangle + label | **polylines/fillPoly** (contour) or rectangle (fallback) + label |

---

## 5. Implementation Details

**vision_ops.py**

- **Model:** Lazy-load `yolov8n-seg.pt`. If seg model fails to load, fall back to `yolov8n.pt` and run in box-only mode (no contour).
- **Mask → contour:** For each detection with a mask (Ultralytics `result.masks`), convert mask to a contour (e.g. `cv2.findContours` on the mask raster, or use Ultralytics’ polygon format if exposed). Store as list of `[x,y]` in image coordinates. Clip to frame bounds.
- **Filtering:** In `_filter_detections`, for each item: if `contour` present, compute area via `cv2.contourArea(contour)` and compare to `frame_area * MAX_BBOX_AREA_FRACTION`; else use bbox area as today.
- **Drawing:** In `draw_overlay`, for each detection: if `contour` present, `cv2.drawContours` or `cv2.fillPoly` (e.g. semi-transparent fill + solid outline); else draw rectangle as today. Label at bbox top-left (or contour centroid) as today.

**app.py**

- No change to stream/API contract. `_workspace_latest_detections` may now contain items with `contour`; overlay and chat already iterate detections and can use contour when present.

**Dependencies**

- No new deps. Ultralytics already supports seg models; `yolov8n-seg.pt` downloads on first use like `yolov8n.pt`.

---

## 6. Error Handling and Fallbacks

- **Seg model load fails:** Load `yolov8n.pt` and run box-only; no contour in output. Log once.
- **Mask missing for a detection:** Use bbox only for filter and overlay (current behavior).
- **Contour empty or invalid:** Skip contour draw; use bbox.
- **CPU slower with seg:** Keep “run detection every Nth frame” (e.g. 5); if FPS drops, increase N or add a config to force box-only model.

---

## 7. Files to Touch

- **inventory/app/vision_ops.py** — model switch to seg, mask→contour extraction, filter by contour/bbox area, overlay with contour/rectangle.
- **inventory/app/app.py** — no structural change; ensure detection list is still used the same way (optional: pass frame shape into filter if needed).
- **docs/plans/** — this design; optional short note in PROJECT_STRUCTURE or README that Workspace uses YOLOv8-seg for mask overlay.

---

## 8. Success Criteria

- Workspace stream with overlay shows **irregular outlines** for objects that have masks (e.g. cell phone, cup, book).
- Objects without usable masks still show **boxes**.
- Mat/large-surface filtering still works (mask area or bbox area).
- No new services or GPU; runs on fs-dev CPU in existing container.
- Chat and procedure focus still work with the same detection list (contour optional).

---

## 9. Out of Scope (this phase)

- Custom-trained or non-COCO models.
- GPU or second-stage “deeper” AI (VLM, etc.).
- Persisting or editing contours; only live overlay and existing APIs.

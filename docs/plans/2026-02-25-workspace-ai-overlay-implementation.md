# Workspace AI Overlay & Object Detection — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add object detection (YOLOv8), server-drawn overlay, AI-generated steps, and a Workspace chat panel so the user can ask "help me do X" / "what's that?" and see steps and highlights on the camera feed.

**Architecture:** Approach 1 — all in Flask. Long-lived camera unchanged; detection runs on frames (background or in stream path); one MJPEG stream with optional overlay; new chat API and chat UI; steps and current-step drive overlay emphasis.

**Tech Stack:** Flask, OpenCV (existing), Ultralytics YOLOv8, existing OpenAI integration; frontend: vanilla JS, CSS flex/grid.

---

## Task 1: Add YOLOv8 dependency and detection helper

**Files:**
- Modify: `inventory/app/requirements.txt`
- Create: `inventory/app/vision_ops.py`

**Step 1.1:** Add `ultralytics` to requirements.

In `inventory/app/requirements.txt`, add a line: `ultralytics>=8.0.0` (or current stable). Keep existing `opencv-python-headless`.

**Step 1.2:** Create `vision_ops.py` with a function that, given a numpy frame (BGR), runs YOLOv8 and returns a list of detections: `[{ "class": str, "confidence": float, "bbox": [x1, y1, x2, y2] }]`. Use a small model (e.g. `yolov8n`) and CPU. Lazy-load the model on first use; cache the model in a module-level variable. Handle ImportError if ultralytics/opencv missing and return `[]`.

**Step 1.3:** Commit.

```bash
git add inventory/app/requirements.txt inventory/app/vision_ops.py
git commit -m "feat(workspace): add YOLOv8 dependency and vision_ops detection helper"
```

---

## Task 2: Wire detection into the stream (latest detections, no overlay yet)

**Files:**
- Modify: `inventory/app/app.py` (workspace section)

**Step 2.1:** In `app.py`, add a module-level `_workspace_latest_detections = []` and `_workspace_detection_lock = threading.Lock()`. In `_gen_workspace_frames()`, after reading a frame under the existing lock, release the lock, then call the detection helper from `vision_ops` on the frame (e.g. every frame or every 5th frame to limit CPU). Under `_workspace_detection_lock`, set `_workspace_latest_detections = result`. Keep yielding the same MJPEG as today (no drawing yet). Ensure the frame passed to detection is a copy if needed so the stream still encodes the same frame.

**Step 2.2:** Add a simple GET endpoint `GET /api/workspace/detections` that returns `{ "detections": _workspace_latest_detections }` (read under the detection lock). Used later by chat and overlay.

**Step 2.3:** Commit.

```bash
git add inventory/app/app.py
git commit -m "feat(workspace): run YOLO on stream frames and expose /api/workspace/detections"
```

---

## Task 3: Draw overlay on frames (boxes + labels)

**Files:**
- Modify: `inventory/app/vision_ops.py`
- Modify: `inventory/app/app.py`

**Step 3.1:** In `vision_ops.py`, add a function `draw_overlay(frame_bgr, detections, current_step_index=None, focus_keyword=None)` that draws bounding boxes and class labels on `frame_bgr` (in-place). If `current_step_index` is not None and `focus_keyword` is set, draw the matching detection(s) with a distinct color/thickness. Return the same frame (modified).

**Step 3.2:** In `app.py`, add optional query param `overlay=1` to `/api/workspace/stream`. When present, in `_gen_workspace_frames()` (or a variant), after getting the frame and updating detections, call `draw_overlay(frame, _workspace_latest_detections)` before encoding to JPEG. Stream the overlaid MJPEG. When `overlay` is 0 or absent, behavior unchanged (raw stream).

**Step 3.3:** Commit.

```bash
git add inventory/app/vision_ops.py inventory/app/app.py
git commit -m "feat(workspace): server-drawn overlay (boxes + labels) via ?overlay=1"
```

---

## Task 4: Workspace chat API (LLM, no steps yet)

**Files:**
- Modify: `inventory/app/app.py`

**Step 4.1:** Add `POST /api/workspace/chat` that accepts JSON `{ "message": "..." }`. Use the existing OpenAI client and API key from config. Send the user message with a short system prompt indicating “you are a lab assistant for a hardware workspace; the user may ask about objects or ask for help with a task.” Return JSON `{ "reply": "..." }`. Do not include detections or steps in context yet; keep it minimal so the endpoint works.

**Step 4.2:** Commit.

```bash
git add inventory/app/app.py
git commit -m "feat(workspace): add POST /api/workspace/chat for LLM replies"
```

---

## Task 5: Chat API with detections and inventory context

**Files:**
- Modify: `inventory/app/app.py`

**Step 5.1:** When building the chat request, read `_workspace_latest_detections` under the lock. Add to the system or user context a short summary of current detections (e.g. “Currently visible: cell phone, book, cup”). If the app has an inventory search or catalog, add a one-line note that “inventory contains boards, tools, etc.” so the LLM can say “check the inventory for X.” No need to run a real inventory query in v1; a static hint is enough. Return `{ "reply": "..." }` as before.

**Step 5.2:** Commit.

```bash
git add inventory/app/app.py
git commit -m "feat(workspace): chat API includes detection summary and inventory hint"
```

---

## Task 6: Step generation and current-step state

**Files:**
- Modify: `inventory/app/app.py`

**Step 6.1:** Add in-memory state (e.g. per-session or global for single user): `_workspace_procedure_steps = []`, `_workspace_current_step_index = 0`. Add `POST /api/workspace/chat` handling so that when the user message clearly asks for a procedure (e.g. “help me flash the T-Beam”), the LLM is prompted to return a JSON array of steps in a single reply, e.g. `[{ "step_index": 1, "text": "Pick up the USB cable", "focus_keyword": "cable" }, ...]`. Parse that and set `_workspace_procedure_steps` and reset `_workspace_current_step_index` to 0. Store in module state for now.

**Step 6.2:** Add `GET /api/workspace/procedure` returning `{ "steps": [...], "current_index": 0 }` and `POST /api/workspace/procedure/step` with body `{ "index": 0 }` to set `_workspace_current_step_index`. Overlay will use this to highlight the step’s focus_keyword.

**Step 6.3:** Commit.

```bash
git add inventory/app/app.py
git commit -m "feat(workspace): step generation from chat and procedure/step API"
```

---

## Task 7: Overlay uses current step for highlight

**Files:**
- Modify: `inventory/app/app.py`
- Modify: `inventory/app/vision_ops.py`

**Step 7.1:** When generating the overlay stream (`overlay=1`), read `_workspace_current_step_index` and `_workspace_procedure_steps`. If there is a current step, pass its `focus_keyword` (and index) to `draw_overlay()` so the matching detection(s) are drawn with emphasis. Already implemented in Task 3; wire the procedure state into the stream generator here.

**Step 7.2:** Commit.

```bash
git add inventory/app/app.py inventory/app/vision_ops.py
git commit -m "feat(workspace): overlay highlights object for current procedure step"
```

---

## Task 8: Workspace layout — chat panel (HTML + CSS)

**Files:**
- Modify: `inventory/app/templates/index.html`
- Modify: `inventory/app/static/css/style.css`

**Step 8.1:** In the Workspace tab section, add a chat container to the right of the camera feed: a scrollable message list (e.g. `#workspace-chat-messages`) and an input + send button (e.g. `#workspace-chat-input`, `#workspace-chat-send`). Use a flex or grid layout so feed and chat sit side-by-side on wide screens.

**Step 8.2:** In CSS, add rules so that below a breakpoint (e.g. 768px) the layout stacks: feed full width, then chat below. Style the message list and input to match the rest of the app.

**Step 8.3:** Commit.

```bash
git add inventory/app/templates/index.html inventory/app/static/css/style.css
git commit -m "feat(workspace): add chat panel layout (right/below feed)"
```

---

## Task 9: Chat UI — send message and display reply

**Files:**
- Modify: `inventory/app/static/js/app.js`

**Step 9.1:** On Workspace tab init or when the chat panel is visible, attach a submit handler to the chat input (or send button). On submit, POST the message to `POST /api/workspace/chat`, then append the user message and the assistant reply to the message list. Disable input while waiting; show a simple “…” for the assistant until the reply arrives. No procedure/step UI yet.

**Step 9.2:** Commit.

```bash
git add inventory/app/static/js/app.js
git commit -m "feat(workspace): chat UI send message and display reply"
```

---

## Task 10: Procedure and current-step UI

**Files:**
- Modify: `inventory/app/templates/index.html`
- Modify: `inventory/app/static/js/app.js`

**Step 10.1:** When the chat reply contains a procedure (backend can return a flag or structured payload, e.g. `{ "reply": "...", "steps": [...] }`), parse steps and render them in the chat or in a small “Procedure” block (e.g. numbered list). Add “Next step” / “Prev step” buttons that call `POST /api/workspace/procedure/step` with the new index and update the overlay (by reloading the stream with the same overlay=1 or by the backend already using the new current_step). Ensure the stream URL or iframe/img is refreshed so the overlay redraws with the new step (e.g. bump a query param when step changes).

**Step 10.2:** Commit.

```bash
git add inventory/app/templates/index.html inventory/app/static/js/app.js
git commit -m "feat(workspace): procedure steps UI and next/prev step with overlay update"
```

---

## Task 11: Overlay toggle in Workspace UI

**Files:**
- Modify: `inventory/app/templates/index.html`
- Modify: `inventory/app/static/js/app.js`

**Step 11.1:** Add an “Overlay on/off” toggle or checkbox in the Workspace controls. When toggled on, set the stream URL to include `overlay=1`; when off, remove it. Re-load the stream (e.g. set `feedEl.src`) when the toggle changes.

**Step 11.2:** Commit.

```bash
git add inventory/app/templates/index.html inventory/app/static/js/app.js
git commit -m "feat(workspace): overlay on/off toggle in UI"
```

---

## Task 12: Inventory-aware hint for “what’s that?” (heuristic)

**Files:**
- Modify: `inventory/app/app.py`

**Step 12.1:** When the user asks a “what’s that?” style question, optionally run a simple inventory search (e.g. by keyword from the question or from detection classes) and include the top 1–3 item names/ids in the context sent to the LLM so the reply can say “this might be the T-Beam 1W from your inventory” with a link or id. Use existing inventory DB/catalog if available; otherwise skip. Document in code that this is a heuristic for v1.

**Step 12.2:** Commit.

```bash
git add inventory/app/app.py
git commit -m "feat(workspace): inventory-aware hint for what's that in chat"
```

---

## Task 13: Documentation and PROJECT_STRUCTURE

**Files:**
- Modify: `PROJECT_STRUCTURE.md`
- Modify: `docs/AGENT_DOCKER_CONTEXT.md` or `inventory/app/README.md` if needed

**Step 13.1:** In PROJECT_STRUCTURE, add a short note under the inventory app or Workspace that the Workspace tab includes object detection (YOLOv8), overlay, and AI chat with step-by-step procedures. List `vision_ops.py` and the new API routes. Update “Last updated” and any dependency list (ultralytics).

**Step 13.2:** Commit.

```bash
git add PROJECT_STRUCTURE.md
git commit -m "docs: PROJECT_STRUCTURE for Workspace AI overlay and object detection"
```

---

## Execution

After implementing, run the app (local or fs-dev), open Workspace, turn overlay on, send a chat message, and request a procedure; confirm steps appear and overlay highlights. Rebuild containers and redeploy to fs-dev if using Docker.

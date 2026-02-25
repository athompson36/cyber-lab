# Workspace AI Interactive Overlay & Object Detection — Design

**Status:** Approved (Approach 1)  
**Date:** 2026-02-25

---

## 1. Goal

Add to the Workspace tab: (A) generic object detection on the camera feed, (B) inventory-aware labels when detections match catalog items, (C) AI-generated step-by-step procedures from natural language in chat, with the overlay highlighting objects and pointing out the current step. A chat panel (right of feed or below on narrow layout) supports “help me do X” (AI returns steps and drives overlay) and “what’s that?” (object info from detections + inventory + LLM). All in the existing Flask app: one stream with server-drawn overlay, YOLOv8 and chat/LLM in-process.

---

## 2. Architecture and Data Flow

- **Camera:** Unchanged. Single long-lived `_workspace_cap` and lock.
- **Detection:** One path (background thread or inline in stream path) that, under the lock, reads frames, runs YOLOv8, and stores “latest detections” (list of `{ class, confidence, bbox }`) and optionally “latest frame.” The stream generator uses this to draw boxes/labels on each frame and yields MJPEG.
- **Overlay:** Server-side drawing: bounding boxes, class labels, and (when a procedure is active) emphasis on the object(s) for the current step. Query param (e.g. `overlay=1`) to enable/disable overlay.
- **Chat:** New panel in the Workspace tab (right of feed on wide layout, below on narrow). Chat UI sends messages to a new endpoint (e.g. `POST /api/workspace/chat`). Backend uses the existing LLM integration with context: recent message, current detections (and any inventory matches), and optional “current procedure steps.”
- **Steps:** When the user says e.g. “Help me flash the T-Beam,” the LLM returns a structured list of steps (e.g. JSON array of `{ step_index, text, focus_keyword }`). Frontend stores steps and “current step” index; backend overlay (or a small API) receives “current step” so the overlay can highlight the right thing. Steps are not persisted in v1; they’re generated per conversation.
- **Object info by request:** User asks “What’s that?” or “Tell me about the multimeter.” Backend uses latest detections + inventory (e.g. match by class or keyword) + LLM to produce a short answer. Optional later: “click on detection” sends bbox or detection id with the message.

---

## 3. UI Layout and Chat

- **Layout:** Workspace tab = camera feed (left or full width) + chat panel (right or below). CSS (flex/grid) + breakpoint so narrow view stacks feed then chat.
- **Chat:** Message list (scrollable) + input. Messages are user + assistant; assistant can be step text, object info, or general reply. Optional: “Start procedure” or “What’s this?” quick actions that prefill the input.
- **Overlay controls:** Toggle overlay on/off; optional “procedure” mode that shows current step number and text (in chat or as overlay caption). No procedure selector dropdown in v1 — procedure is created from natural language in chat.

---

## 4. Tech Choices and Scope

- **Model:** YOLOv8 (e.g. `ultralytics`), small or medium; run in Flask process. CPU first; GPU optional later.
- **LLM:** Existing OpenAI integration (or same pattern) for chat and step generation; same API key as rest of app.
- **Inventory matching:** Heuristic in v1: map YOLO classes to catalog categories or keywords; optional simple text match on item names/descriptions. No custom-trained model for “T-Beam” in v1 — generic detection + LLM + inventory search to answer “what’s that?”
- **Out of scope for v1:** Stored/editable procedures (file-based), projection, multiple cameras, voice.

---

## 5. Error Handling and Fallbacks

- **No YOLO/opencv:** Overlay off; stream remains raw MJPEG; chat still works for non-vision answers.
- **No API key:** Chat returns a clear “OpenAI key not set” message; steps and object-info need key.
- **Detection slow:** Run detection at reduced rate (e.g. every Nth frame) so stream FPS stays usable; overlay uses last available detections.

---

## 6. Files and Areas to Touch

- **Backend:** `inventory/app/app.py` — workspace routes, stream generator with overlay, new `/api/workspace/chat`, step/current-step state or API; optional `inventory/app/vision_ops.py` for YOLO + overlay drawing.
- **Frontend:** `inventory/app/templates/index.html` — Workspace section layout (feed + chat panel); `inventory/app/static/js/app.js` — chat UI, overlay toggle, current-step handling; `inventory/app/static/css/style.css` — layout and chat styling.
- **Dependencies:** `inventory/app/requirements.txt` — add `ultralytics` (YOLOv8); existing `opencv-python-headless` and OpenAI.

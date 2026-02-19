# MeshCore Upstream Roadmap — Lab Tracking

Tracks MeshCore upstream features (from `ripplebiz/MeshCore` README "Road-Map / To-Do") that affect this lab or T-Beam 1W builds. Update this when upstream releases new features.

**Upstream repo:** `https://github.com/ripplebiz/MeshCore`  
**Local clone:** `devices/t_beam_1w/firmware/meshcore/repo`

---

## Tracked Items

| ID  | Feature | Upstream Status | Lab Impact |
|-----|---------|----------------|------------|
| MC1 | Repeater/Bridge: standardise Transport Codes (zoning/filtering) | Planned | Re-test repeater builds; may need config changes |
| MC2 | Core: round-trip manual path support | Planned | Track |
| MC3 | Companion + Apps: multiple sub-meshes, off-grid client repeat | Planned | May need app + firmware matrix update |
| MC4 | Core + Apps: LZW message compression | Planned | Track; rebuild and test |
| MC5 | Core: dynamic CR for weak vs strong hops | Planned | Track |
| MC6 | Core: multiple virtual nodes on one device | Planned | Track; test on T-Beam 1W |
| MC7 | V2 protocol: path hashes, new encryption | Planned | May affect overlays and patches |

---

## Version Compatibility

| Lab firmware version | MeshCore upstream commit/tag | Compatible apps | Notes |
|---------------------|------------------------------|-----------------|-------|
| _Current_ | main (as of submodule pin) | MeshCore Android/iOS | Working: companion, room server, repeater |

---

## When Upstream Updates

1. Pull latest in `devices/t_beam_1w/firmware/meshcore/repo`.
2. Check if overlays/patches still apply cleanly.
3. Rebuild all three variants via `./scripts/lab-build.sh t_beam_1w meshcore <env>`.
4. Run hardware smoke test (serial output, BLE, LoRa TX/RX).
5. Update this table with new commit/tag and any compatibility notes.

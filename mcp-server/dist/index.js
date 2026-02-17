#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListResourcesRequestSchema, ListToolsRequestSchema, ReadResourceRequestSchema, } from "@modelcontextprotocol/sdk/types.js";
import * as fs from "fs";
import * as path from "path";
const REPO_ROOT = process.env.ESP32_LAB_REPO_ROOT || process.cwd();
function readFileSafe(relativePath) {
    const full = path.join(REPO_ROOT, relativePath);
    try {
        return fs.readFileSync(full, "utf-8");
    }
    catch {
        return `(File not found: ${relativePath})`;
    }
}
function listDevicesDir() {
    const devicesPath = path.join(REPO_ROOT, "devices");
    try {
        const entries = fs.readdirSync(devicesPath, { withFileTypes: true });
        return entries.filter((e) => e.isDirectory()).map((e) => e.name);
    }
    catch {
        return [];
    }
}
function listInventoryCategories() {
    const itemsPath = path.join(REPO_ROOT, "inventory", "items");
    try {
        const entries = fs.readdirSync(itemsPath, { withFileTypes: true });
        return entries.filter((e) => e.isFile() && e.name.endsWith(".yaml")).map((e) => e.name.replace(".yaml", ""));
    }
    catch {
        return [];
    }
}
const server = new Server({
    name: "esp32-lab-mcp-server",
    version: "1.0.0",
}, {
    capabilities: {
        resources: {},
        tools: {},
    },
});
// --- Resources ---
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
    resources: [
        { uri: "project://context", name: "Project context (current phase, next actions)", mimeType: "text/markdown" },
        { uri: "project://roadmap", name: "Roadmap summary and priorities", mimeType: "text/markdown" },
        { uri: "project://development-plan", name: "Development plan (phases and tasks)", mimeType: "text/markdown" },
        { uri: "project://lab-context", name: "Lab rules and contract (CONTEXT)", mimeType: "text/markdown" },
        { uri: "project://inventory", name: "Inventory catalog (SBCs, controllers, sensors, components)", mimeType: "text/markdown" },
        { uri: "project://firmware-index", name: "Firmware index per device (repos and builds)", mimeType: "text/markdown" },
        { uri: "project://repos", name: "Lab repo index (Meshtastic, MeshCore, Launcher, etc.)", mimeType: "text/markdown" },
    ],
}));
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    const uri = request.params.uri;
    let content;
    switch (uri) {
        case "project://context":
            content = readFileSafe("PROJECT_CONTEXT.md");
            break;
        case "project://roadmap":
            content = readFileSafe("FEATURE_ROADMAP.md");
            break;
        case "project://development-plan":
            content = readFileSafe("DEVELOPMENT_PLAN.md");
            break;
        case "project://lab-context":
            content = readFileSafe("CONTEXT.md");
            break;
        case "project://inventory":
            content = readFileSafe("inventory/README.md");
            break;
        case "project://firmware-index":
            content = readFileSafe("FIRMWARE_INDEX.md");
            break;
        case "project://repos":
            content = readFileSafe("REPOS.md");
            break;
        default:
            content = `Unknown resource: ${uri}`;
    }
    return { contents: [{ uri, mimeType: "text/markdown", text: content }] };
});
// --- Tools ---
server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
        {
            name: "get_project_status",
            description: "Return current phase, next actions, and priority focus from PROJECT_CONTEXT.md. Use to stay on task.",
            inputSchema: { type: "object", properties: {} },
        },
        {
            name: "get_next_tasks",
            description: "Return the next uncompleted tasks from DEVELOPMENT_PLAN.md for the current phase.",
            inputSchema: { type: "object", properties: {} },
        },
        {
            name: "get_device_context",
            description: "Return device context and SDK/tools for a given device (e.g. t_beam_1w, raspberry_pi_v4).",
            inputSchema: {
                type: "object",
                properties: {
                    device_id: { type: "string", description: "Device ID (e.g. t_beam_1w, t_deck_plus)" },
                },
                required: ["device_id"],
            },
        },
        {
            name: "list_devices",
            description: "List all device IDs in devices/.",
            inputSchema: { type: "object", properties: {} },
        },
        {
            name: "get_inventory_summary",
            description: "Return a short summary of the lab inventory: README plus list of catalog categories (sbcs, controllers, sensors, accessories, components).",
            inputSchema: { type: "object", properties: {} },
        },
    ],
}));
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    const arg = (args || {});
    switch (name) {
        case "get_project_status": {
            const text = readFileSafe("PROJECT_CONTEXT.md");
            return { content: [{ type: "text", text }] };
        }
        case "get_next_tasks": {
            const text = readFileSafe("DEVELOPMENT_PLAN.md");
            return { content: [{ type: "text", text }] };
        }
        case "get_device_context": {
            const deviceId = arg.device_id;
            if (!deviceId)
                return { content: [{ type: "text", text: "Error: device_id required" }], isError: true };
            const base = path.join("devices", deviceId);
            const ctx = readFileSafe(path.join(base, "DEVICE_CONTEXT.md"));
            const sdk = readFileSafe(path.join(base, "notes", "SDK_AND_TOOLS.md"));
            const firmware = readFileSafe(path.join(base, "firmware", "README.md"));
            const text = `## DEVICE_CONTEXT\n\n${ctx}\n\n## SDK_AND_TOOLS\n\n${sdk}\n\n## FIRMWARE\n\n${firmware}`;
            return { content: [{ type: "text", text }] };
        }
        case "list_devices": {
            const devices = listDevicesDir();
            const text = devices.length ? devices.join("\n") : "(No devices directory or empty)";
            return { content: [{ type: "text", text }] };
        }
        case "get_inventory_summary": {
            const readme = readFileSafe("inventory/README.md");
            const categories = listInventoryCategories();
            const text = `${readme}\n\n## Catalog categories\n${categories.length ? categories.join(", ") : "(none)"}`;
            return { content: [{ type: "text", text }] };
        }
        default:
            return { content: [{ type: "text", text: `Unknown tool: ${name}` }], isError: true };
    }
});
// --- Run ---
async function main() {
    const repoRoot = process.env.ESP32_LAB_REPO_ROOT || process.cwd();
    if (!fs.existsSync(repoRoot)) {
        console.error(`[esp32-lab-mcp] REPO_ROOT does not exist: ${repoRoot}`);
        process.exit(1);
    }
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("[esp32-lab-mcp] Server running on stdio (repo: " + repoRoot + ")");
}
main().catch((err) => {
    console.error("[esp32-lab-mcp] Fatal:", err instanceof Error ? err.message : String(err));
    process.exit(1);
});

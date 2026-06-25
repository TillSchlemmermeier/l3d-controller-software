import { ipcRenderer, contextBridge } from 'electron'

// One-way event handlers (main -> renderer)
type EventCallback = (data: any) => void
// Every on* method returns a Disposer that removes ONLY its own listener.
type Disposer = () => void

// These are the ONLY IPC channels the renderer is permitted to touch.

// main -> renderer (subscribed to via ipcRenderer.on)
const RECEIVE_CHANNELS = {
  CUBE_BINARY: 'cube_data_binary',
  SPECTRUM: 'spectrum_data',
  STATE: 'state',
  STATE_SECTION: 'state_section',
  STATE_KEY: 'state_key',
  PYTHON_OUTPUT: 'python-output',
  WS_CONNECTED: 'ws-connected',
  WS_DISCONNECTED: 'ws-disconnected',
  WS_ERROR: 'ws-error',
  REINIT_RENDERERS: 'reinitialize-renderers',
} as const

const INVOKE_CHANNELS = {
  RESTART_BACKEND: 'restart-backend',
} as const

// Subscribe to a fixed channel, forwarding only the payload to the callback.
// Returns a disposer that removes exactly THIS registration's listener
const subscribe = (channel: string) => (callback: EventCallback): Disposer => {
  const listener = (_event: Electron.IpcRendererEvent, data: any) => callback(data)
  ipcRenderer.on(channel, listener)
  return () => ipcRenderer.off(channel, listener)
}

contextBridge.exposeInMainWorld('ipcRenderer', {
  restartBackend: () => ipcRenderer.invoke(INVOKE_CHANNELS.RESTART_BACKEND),

  // --- data streams (main -> renderer) ---
  onCubeData: subscribe(RECEIVE_CHANNELS.CUBE_BINARY),
  onSpectrumData: subscribe(RECEIVE_CHANNELS.SPECTRUM),
  onStateData: subscribe(RECEIVE_CHANNELS.STATE),
  onStateSectionData: subscribe(RECEIVE_CHANNELS.STATE_SECTION),
  onStateKeyData: subscribe(RECEIVE_CHANNELS.STATE_KEY),
  // python-output keeps the raw (event, data) signature; still returns a disposer.
  onPythonOutput: (callback: (event: any, data: any) => void): Disposer => {
    ipcRenderer.on(RECEIVE_CHANNELS.PYTHON_OUTPUT, callback)
    return () => ipcRenderer.off(RECEIVE_CHANNELS.PYTHON_OUTPUT, callback)
  },

  // --- connection lifecycle (main -> renderer) ---
  onWebSocketConnected: subscribe(RECEIVE_CHANNELS.WS_CONNECTED),
  onWebSocketDisconnected: subscribe(RECEIVE_CHANNELS.WS_DISCONNECTED),
  onWebSocketError: subscribe(RECEIVE_CHANNELS.WS_ERROR),
  // fired by main after a backend restart, once the new ws is up
  onReinitializeRenderers: subscribe(RECEIVE_CHANNELS.REINIT_RENDERERS),
})

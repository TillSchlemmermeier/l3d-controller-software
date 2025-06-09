import { ipcRenderer, contextBridge } from 'electron'

// Define type for event handlers
type EventCallback = (data: any) => void

// Available channels
const CHANNELS = {
  CUBE: 'cube_data',
  SPECTRUM: 'spectrum_data',
  STATE: 'state',
  STATE_SECTION: 'state_section',
  STATE_KEY: 'state_key',
  WS_DATA: 'websocket-data',
  WS_READY: 'ws-ready'
} as const

// Create event handler registration
const createEventHandler = (channel: string, logMessage: string) => {
  return (callback: EventCallback) => {
    console.log(logMessage)
    ipcRenderer.on(channel, (_event, data) => callback(data))
  }
}

// Expose API to renderer process
contextBridge.exposeInMainWorld('ipcRenderer', {
  // Basic IPC methods
  send: (channel: string, ...args: any[]) => ipcRenderer.send(channel, ...args),
  invoke: (channel: string, ...args: any[]) => ipcRenderer.invoke(channel, ...args),
  off: (channel: string, listener?: (...args: any[]) => void) => {
    if (listener) {
      ipcRenderer.off(channel, listener);
    }
  },
  restartBackend: () => ipcRenderer.invoke('restart-backend'),

  // WebSocket ready handler
  on: (channel: string, func: EventCallback) => {
    if (channel === CHANNELS.WS_READY) {
      ipcRenderer.on(channel, (_event: Electron.IpcRendererEvent, data: any) => func(data))
    }
  },

  // Data handlers
  onCubeData: createEventHandler(
    CHANNELS.CUBE, 
    'Registering Cube data handler'
  ),
  onSpectrumData: createEventHandler(
    CHANNELS.SPECTRUM, 
    'Registering Spectrum data handler'
  ),
  onStateData: createEventHandler(
    CHANNELS.STATE, 
    'Registering State data handler'
  ),
  onStateSectionData: createEventHandler(
    CHANNELS.STATE_SECTION, 
    'Registering State Section data handler'
  ),
  onStateKeyData: createEventHandler(
    CHANNELS.STATE_KEY, 
    'Registering State Key data handler'
  ),
  onWebSocketData: createEventHandler(
    CHANNELS.WS_DATA, 
    'Registering websocket data handler'
  ),

  // Cleanup
  removeWebSocketListener: () => {
    console.log('Removing websocket listener')
    ipcRenderer.removeAllListeners(CHANNELS.WS_DATA)
  }
})
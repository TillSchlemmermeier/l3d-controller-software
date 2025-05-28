"use strict";
const electron = require("electron");
const CHANNELS = {
  CUBE: "cube_data",
  SPECTRUM: "spectrum_data",
  STATE: "state",
  STATE_SECTION: "state_section",
  STATE_KEY: "state_key",
  WS_DATA: "websocket-data",
  WS_READY: "ws-ready"
};
const createEventHandler = (channel, logMessage) => {
  return (callback) => {
    console.log(logMessage);
    electron.ipcRenderer.on(channel, (_event, data) => callback(data));
  };
};
electron.contextBridge.exposeInMainWorld("ipcRenderer", {
  // Basic IPC methods
  send: (channel, ...args) => electron.ipcRenderer.send(channel, ...args),
  invoke: (channel, ...args) => electron.ipcRenderer.invoke(channel, ...args),
  off: (channel, listener) => {
    if (listener) {
      electron.ipcRenderer.off(channel, listener);
    }
  },
  // WebSocket ready handler
  on: (channel, func) => {
    if (channel === CHANNELS.WS_READY) {
      electron.ipcRenderer.on(channel, (_event, data) => func(data));
    }
  },
  // Data handlers
  onCubeData: createEventHandler(
    CHANNELS.CUBE,
    "Registering Cube data handler"
  ),
  onSpectrumData: createEventHandler(
    CHANNELS.SPECTRUM,
    "Registering Spectrum data handler"
  ),
  onStateData: createEventHandler(
    CHANNELS.STATE,
    "Registering State data handler"
  ),
  onStateSectionData: createEventHandler(
    CHANNELS.STATE_SECTION,
    "Registering State Section data handler"
  ),
  onStateKeyData: createEventHandler(
    CHANNELS.STATE_KEY,
    "Registering State Key data handler"
  ),
  onWebSocketData: createEventHandler(
    CHANNELS.WS_DATA,
    "Registering websocket data handler"
  ),
  // Cleanup
  removeWebSocketListener: () => {
    console.log("Removing websocket listener");
    electron.ipcRenderer.removeAllListeners(CHANNELS.WS_DATA);
  }
});

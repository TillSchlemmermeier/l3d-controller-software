// Each on* registration returns a disposer that removes only that listener.
type Disposer = () => void;

interface IpcRenderer {
  // request/response (renderer -> main)
  restartBackend: () => Promise<void>;
  // data streams (main -> renderer) — call the returned disposer to unsubscribe
  onCubeData(callback: (data: any) => void): Disposer;
  onSpectrumData(callback: (data: any) => void): Disposer;
  onStateData(callback: (data: any) => void): Disposer;
  onStateSectionData(callback: (data: any) => void): Disposer;
  onStateKeyData(callback: (data: any) => void): Disposer;
  onPythonOutput(callback: (event: any, data: any) => void): Disposer;
  // connection lifecycle (main -> renderer)
  onWebSocketConnected(callback: () => void): Disposer;
  onWebSocketDisconnected(callback: () => void): Disposer;
  onWebSocketError(callback: (error: string) => void): Disposer;
  onReinitializeRenderers(callback: () => void): Disposer;
}

declare global {
  interface Window {
    ipcRenderer: IpcRenderer;
  }
}

export {};
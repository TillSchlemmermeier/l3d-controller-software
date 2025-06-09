interface IpcRenderer {
  onCubeData(callback: (data: any) => void): void;
  onSpectrumData(callback: (data: any) => void): void;
  onStateData(callback: (data: any) => void): void;
  onStateSectionData(callback: (data: any) => void): void;
  onStateKeyData(callback: (data: any) => void): void;
  on(channel: string, listener: (event: any, ...args: any[]) => void): void;
  off(channel: string, listener: (...args: any[]) => void): void;
  send(channel: string, ...args: any[]): void;
  invoke(channel: string, ...args: any[]): Promise<any>;
  onWebSocketData(callback: (data: any) => void): void;
  removeWebSocketListener(): void;
  restartBackend: () => Promise<void>;
}
interface Window {
  ipcRenderer: IpcRenderer;
}
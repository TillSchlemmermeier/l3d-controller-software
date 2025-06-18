import { app, BrowserWindow, ipcMain } from 'electron'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import WebSocket from 'ws'
import { exec, spawn } from 'child_process'

const APP_ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..')
const VITE_DEV_SERVER_URL = process.env['VITE_DEV_SERVER_URL']
const RENDERER_DIST = path.join(APP_ROOT, 'dist')
const PUBLIC_PATH = VITE_DEV_SERVER_URL ? path.join(APP_ROOT, 'public') : RENDERER_DIST

let ws: WebSocket | null = null
let win: BrowserWindow | null = null
let isQuitting = false
let isProcessing = false;

function setupWebSocket(win: BrowserWindow) {
  ws = new WebSocket('ws://localhost:8000/ws')

  ws.on('open', () => {
    console.log('WebSocket connection opened')
    win.webContents.send('ws-connected')
  })

  ws.on('error', (error) => {
    console.error('WebSocket error:', error)
    win.webContents.send('ws-error', error.message)
  })

  ws.on('message', (data: Buffer) => {
    // drop messages to prevent memory buildup when app is out of focus
    if (isProcessing) {
      return
    }
    try {
      isProcessing = true;
      const message = JSON.parse(data.toString())
      win?.webContents.send(message.type, message.data)
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error)
    } finally {
      isProcessing = false;
    }
  })

  ws.on('close', () => {
    console.log('WebSocket connection closed')
    win.webContents.send('ws-disconnected')
    if (!isQuitting) {
      setTimeout(() => {
        console.log('Attempting WebSocket reconnection...')
        setupWebSocket(win)
      }, 3000)
    }
  })
}

function setupPythonProcess(restore = false) {
  const pythonPath = path.join(APP_ROOT, 'core')
  const process = spawn('python3.12', ['-u', 'main.py', ...(restore ? ['--restore'] : [])], {
    cwd: pythonPath,
    stdio: ['ignore', 'pipe', 'pipe']
  })

  // Set up console output handlers
  process.stdout.on('data', (data: Buffer) => {
    const lines = data.toString().split('\n')
    lines.forEach(line => {
      if (line.trim()) {
        console.log(`[CORE] ${line}`)
      }
    })
    win?.webContents.send('python-output', {
      type: 'stdout',
      data: data.toString()
    })
  })

  process.stderr.on('data', (data: Buffer) => {
    const lines = data.toString().split('\n')
    lines.forEach(line => {
      if (line.trim()) {
        console.error(`[CORE] ${line}`)
      }
    })
    win?.webContents.send('python-output', {
      type: 'stderr',
      data: data.toString()
    })
  })

  return process
}

function createWindow() {
  return new BrowserWindow({
    width: 2560,
    height: 1440,
    backgroundColor: '#3f3f46',
    frame: false,  // Remove window frame
    titleBarStyle: 'hidden', // Hide title bar
    resizable: false, // Prevent resizing
    minimizable: false, // Optionally prevent minimizing
    maximizable: false, // Prevent maximizing
    fullscreenable: true, // Prevent fullscreen
    fullscreen: true,
    // x: 200,
    // y: 200,
    icon: path.join(PUBLIC_PATH, 'icons/brightness.svg'),
    webPreferences: {
      preload: path.join(APP_ROOT, 'dist-electron', 'preload.mjs'),
    },
  })
}

function restartBackend() {
  // Close existing WebSocket connection
  if (ws) {
    ws.removeAllListeners()
    ws.close()
    ws = null
  }
  // Kill backend processes and restart
  exec('killall python3.12', () => {
    // Wait for processes to terminate
    setTimeout(() => {
      setupPythonProcess(true)
      // reestablish WebSocket connection
      setTimeout(() => {
        if (win) {
          setupWebSocket(win)
          win.webContents.send('reinitialize-renderers')
        }
      }, 1500)
      console.log('Backend restarting...')
    }, 500)
  })
}

ipcMain.handle('restart-backend', () => {
  restartBackend()
})

// App Event Handlers
app.on('window-all-closed', () => {
  isQuitting = true
  if (ws) {
    ws.removeAllListeners()
    ws.close()
    ws = null
  }
  exec('killall python3.12')
  win = null
  app.quit()
})

app.whenReady().then(() => {
  setupPythonProcess()
  win = createWindow()
  win.loadURL(VITE_DEV_SERVER_URL ?? path.join(RENDERER_DIST, 'index.html'))
  setupWebSocket(win)
})
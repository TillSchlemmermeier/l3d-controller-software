import { app, BrowserWindow, ipcMain } from 'electron'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import WebSocket from 'ws'
import { exec } from 'child_process'

const APP_ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..')
const VITE_DEV_SERVER_URL = process.env['VITE_DEV_SERVER_URL']
const RENDERER_DIST = path.join(APP_ROOT, 'dist')
const PUBLIC_PATH = VITE_DEV_SERVER_URL ? path.join(APP_ROOT, 'public') : RENDERER_DIST

let ws: WebSocket | null = null
let win: BrowserWindow | null = null
let isQuitting = false

function setupWebSocket(win: BrowserWindow) {
  ws = new WebSocket('ws://localhost:8000/ws')

  ws.on('open', () => console.log('WebSocket connection opened'))
  
  ws.on('error', (error) => {
    console.error('WebSocket error:', error)
    win.webContents.send('ws-error', error.message)
  })

  ws.on('message', (data: Buffer) => {
    try {
      const message = JSON.parse(data.toString())
      win?.webContents.send(message.type, message.data)
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error)
    }
  })

  ws.on('close', () => {
    console.log('WebSocket connection closed')
    if (!isQuitting) {
      setTimeout(() => {
        console.log('Attempting WebSocket reconnection...')
        setupWebSocket(win)
      }, 3000)
    }
  })
}

function createWindow() {
  return new BrowserWindow({
    width: 2086,
    height: 1300,
    backgroundColor: '#3f3f46',
    // frame: false,  // Remove window frame
    // titleBarStyle: 'hidden', // Hide title bar
    // resizable: false, // Prevent resizing
    // minimizable: false, // Optionally prevent minimizing
    // maximizable: false, // Prevent maximizing
    // fullscreenable: false, // Prevent fullscreen
    x: 200,
    y: 200,
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
      const corePath = path.join(APP_ROOT, 'core')
      exec(`cd "${corePath}" && python3.12 -u main.py`)
      // reestablish WebSocket connection
      setTimeout(() => {
        if (win) {
          setupWebSocket(win)
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
  win = createWindow()
  win.loadURL(VITE_DEV_SERVER_URL ?? path.join(RENDERER_DIST, 'index.html'))
  setupWebSocket(win)
})
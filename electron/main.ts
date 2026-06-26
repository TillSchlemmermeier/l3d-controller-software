import { app, BrowserWindow, ipcMain } from 'electron'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import WebSocket from 'ws'
import { exec, spawn, ChildProcess } from 'child_process'

const APP_ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..')
const VITE_DEV_SERVER_URL = process.env['VITE_DEV_SERVER_URL']
const RENDERER_DIST = path.join(APP_ROOT, 'dist')
const PUBLIC_PATH = VITE_DEV_SERVER_URL ? path.join(APP_ROOT, 'public') : RENDERER_DIST

let ws: WebSocket | null = null
let win: BrowserWindow | null = null
let pythonProcess: ChildProcess | null = null
let isQuitting = false

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

  ws.on('message', (data: any, isBinary: boolean) => {
    // Handle binary cube data separately
    if (isBinary) {
      win.webContents.send('cube_data_binary', data)
      return
    }
    const message = JSON.parse(data.toString())
    win.webContents.send(message.type, message.data)
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
  pythonProcess = spawn('python3.12', ['-u', 'main.py', ...(restore ? ['--restore'] : [])], {
    cwd: pythonPath,
    stdio: ['ignore', 'pipe', 'pipe']
  })

  // Set up console output handlers
  if (pythonProcess.stdout) {
    pythonProcess.stdout.on('data', (data: Buffer) => {
      const lines = data.toString().split('\n')
      lines.forEach(line => {
        if (line.trim()) {
          console.log(`[CORE] ${line}`)
        }
      })

      if (win && !win.isDestroyed()) {
        win.webContents.send('python-output', {
          type: 'stdout',
          data: data.toString()
        })
      }
    })
  }

  if (pythonProcess.stderr) {
    pythonProcess.stderr.on('data', (data: Buffer) => {
      const lines = data.toString().split('\n')
      lines.forEach(line => {
        if (line.trim()) {
          console.error(`[CORE] ${line}`)
        }
      })

      if (win && !win.isDestroyed()) {
        win.webContents.send('python-output', {
          type: 'stderr',
          data: data.toString()
        })
      }
    })
  }
  // Clear reference when process exits
  pythonProcess.on('exit', () => {
    pythonProcess = null
  })

  return pythonProcess
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
      contextIsolation: true,
      nodeIntegration: false,
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
  const startNewProcess = () => {
    setTimeout(() => {
      setupPythonProcess(true)
      setTimeout(() => {
        if (win && !win.isDestroyed()) {
          setupWebSocket(win)
          win.webContents.send('reinitialize-renderers')
        }
      }, 1500)
      console.log('Backend restarting...')
    }, 500)
  }

  // Gracefully kill the process
  if (pythonProcess) {
    pythonProcess.once('exit', startNewProcess)
    pythonProcess.kill('SIGINT')
  } else {
    // Fallback if reference is lost
    exec('killall python3.12', startNewProcess)
  }
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

  if (pythonProcess) {
    console.log('Sending SIGINT to Python...')

    // 1. Listen for the process to actually exit
    pythonProcess.once('exit', () => {
      console.log('================================================')
      console.log('Python process exited cleanly. Quitting Electron.')
      win = null
      app.quit()
    })

    // 2. Send the polite kill signal
    pythonProcess.kill('SIGINT')

    // 3. Safety net: Force quit if Python hangs for more than 2 seconds
    setTimeout(() => {
      console.log('Python took too long to close. Force quitting.')
      app.quit()
    }, 2000)

  } else {
    // Fallback if process is already dead
    exec('killall python3.12', () => {
      win = null
      app.quit()
    })
  }
})

app.whenReady().then(() => {
  setupPythonProcess()
  win = createWindow()
  win.loadURL(VITE_DEV_SERVER_URL ?? path.join(RENDERER_DIST, 'index.html'))
  // wait 2 seconds before setting up WebSocket to allow backend to start
  setTimeout(() => {
    if (win) {
      setupWebSocket(win)
    }
  }, 2000)
})
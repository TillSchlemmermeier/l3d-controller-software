<template>
  <div class="flex flex-row w-[1470px] h-[170px]">
    <div
      v-for="n in 8"
      :key="n"
      :ref="el => scatterplots[n-1] = el as HTMLDivElement"
      class="w-[170px] h-[170px]">
    </div>
    <!-- scatterplot for saving global presets -->
    <div ref="el => scatterplots[8] = el" class="w-[170px] h-[170px] hidden"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted, watch } from 'vue'
import { useCoreStateStore } from '../stores/coreState'
import * as THREE from 'three'

const coreState = useCoreStateStore()
const channelLength = ref(0)
const isCapturing = ref(true)
const capturingGlobalPreset = ref(false)

const scatterplots = ref<(HTMLDivElement | null)[]>([])
const geometries = ref<THREE.BufferGeometry[]>([])
const renderers: THREE.WebGLRenderer[] = []
const scenes: THREE.Scene[] = []
const cameras: THREE.PerspectiveCamera[] = []
const points: THREE.Points[] = []


function captureFrame(renderer: THREE.WebGLRenderer): string {
  return renderer.domElement.toDataURL('image/png')
}

async function captureCombinedView(onFrameCapture: (frame: string) => void): Promise<string[]> {
  capturingGlobalPreset.value = true
  const frames = await captureFrames(8, onFrameCapture)
  capturingGlobalPreset.value = false
  return frames
}

async function captureFrames(channelIndex: number, onFrameCapture: (frame: string) => void): Promise<string[]> {
  console.log('Capturing frames for channel:', channelIndex)
  const frames: string[] = []
  isCapturing.value = true

  // Use 40ms for 25fps (1000ms / 25fps = 40ms)
  const frameInterval = 40

  // Capture 120 frames (4 seconds at 25fps)
  for (let i = 0; i < 120 && isCapturing.value; i++) {
    renderers[channelIndex].render(scenes[channelIndex], cameras[channelIndex])
    const frame = captureFrame(renderers[channelIndex])
    frames.push(frame)
    onFrameCapture(frame) // Call callback with new frame
    await new Promise(resolve => setTimeout(resolve, frameInterval))
  }
  return frames
}

function stopCapture() {
  isCapturing.value = false
}

defineExpose({
  captureFrames,
  captureCombinedView,
  stopCapture
})


function setupScene() {
  const scene = new THREE.Scene()

  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000)
  // camera.position.set(15, 7, 12)  // x: right, y: up, z: forward
  // camera.lookAt(0, -1, 0) // Look at the center of the cube
  camera.position.set(-7, 14.5, 11.5)  // x: right, y: up, z: forward
  camera.up.set(-1, 0, 0) 
  camera.lookAt(1, 0, 0)
  const renderer = new THREE.WebGLRenderer()
  renderer.setSize(170, 170)

  return { scene, camera, renderer }
}

function createVertices() {
  const vertices = []
  for (let i = 0; i < 10; i++) {
    for (let j = 0; j < 10; j++) {
      for (let k = 0; k < 10; k++) {
        vertices.push(i - 4.5, j - 4.5, k - 4.5)
      }
    }
  }
  return vertices
}

function createCircleTexture(): THREE.Texture {
  const canvas = document.createElement('canvas')
  canvas.width = 64
  canvas.height = 64
  
  const context = canvas.getContext('2d')
  if (!context) throw new Error('Could not get 2D context')
  
  context.beginPath()
  context.arc(32, 32, 30, 0, Math.PI * 2)
  context.closePath()
  context.fillStyle = '#ffffff'
  context.fill()
  
  return new THREE.CanvasTexture(canvas)
}

// Share texture across all renderers to save memory
const circleTexture = createCircleTexture()

function updateGeometryColors(geometry: THREE.BufferGeometry, data: any) {
  const colors = new Float32Array(1000 * 3)
  for (let i = 0; i < 1000; i++) {
    colors[i * 3] = data[i][0]     // R
    colors[i * 3 + 1] = data[i][1] // G
    colors[i * 3 + 2] = data[i][2] // B
  }
  geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3))
}

function handleCubeData(message: any) {
  // Handle regular channels
  for (let index = 0; index < channelLength.value; index++) {
    updateGeometryColors(geometries.value[index], message[index + 1])
  }
  // Handle combined view data only when capturing frames for gif
  if (capturingGlobalPreset.value) {
    updateGeometryColors(geometries.value[8], message[0])
  }
}

function initializeRenderers() {
  renderers.forEach(renderer => {
    renderer.dispose()
    renderer.forceContextLoss()
  })

  for (let plot = 0; plot < 9; plot++) {
    const { scene, camera, renderer } = setupScene()
    scenes.push(scene)
    cameras.push(camera)
    renderers.push(renderer)

    if (scatterplots.value[plot]) {
      scatterplots.value[plot]?.appendChild(renderer.domElement)
    }

    const geometry = new THREE.BufferGeometry()
    geometry.setAttribute(
      'position',
      new THREE.Float32BufferAttribute(createVertices(), 3)
    )
    geometries.value.push(geometry)

    const material = new THREE.PointsMaterial({
      size: 1.0,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      map: circleTexture,
      alphaMap: circleTexture,
      alphaTest: 0.1,
      sizeAttenuation: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    })
    const point = new THREE.Points(geometry, material)
    points.push(point)
    scene.add(point)
  }
 
  const animate = () => {
    requestAnimationFrame(animate)
    renderers.forEach((renderer, index) => {
      if (index < 8 || (index === 8 && capturingGlobalPreset.value)) {
        renderer.render(scenes[index], cameras[index])
      }
    })
  }
  animate()
}

onMounted(() => {
  if (!window.ipcRenderer) {
    console.error('Electron API not available')
    return
  }
  channelLength.value = coreState.channels.length
  window.ipcRenderer.onCubeData(handleCubeData)
  initializeRenderers()
})

watch(
  () => coreState.channels.length,
  (newLength) => {
    if (newLength < channelLength.value) {
      for (let i = newLength; i < channelLength.value; i++) {
        if (geometries.value[i]) {
          const emptyColors = new Float32Array(1000 * 3).fill(0)
          geometries.value[i].setAttribute('color', new THREE.Float32BufferAttribute(emptyColors, 3))
          renderers[i].render(scenes[i], cameras[i])
        }
      }
    }
    channelLength.value = newLength
  }
)

onUnmounted(() => {
  window.ipcRenderer.removeWebSocketListener()
  renderers.forEach(renderer => {
    renderer.dispose()
    renderer.forceContextLoss()
    const gl = renderer.domElement.getContext('webgl')
    if (gl) {
      gl.getExtension('WEBGL_lose_context')?.loseContext()
    }
  })
})
</script>
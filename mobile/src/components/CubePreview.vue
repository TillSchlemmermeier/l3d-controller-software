<template>
  <div class="w-full h-full relative bg-black overflow-hidden rounded-2xl shadow-inner shadow-zinc-800">
    <div ref="container" class="w-full h-full" @click="handleCanvasClick"></div>
    
    <!-- Connection Status (Controlled by prop now, or removed if handled in App) -->
    <!-- <div 
      class="absolute top-3 right-14 w-2 h-2 rounded-full transition-colors duration-300 z-50"
      :class="isConnected ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]' : 'bg-red-500 animate-pulse'"
    ></div> -->
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import * as THREE from 'three'

const props = defineProps({
  channel: { type: Number, default: 0 },
  isConnected: { type: Boolean, default: false } // Receive status from App
})

const container = ref<HTMLDivElement | null>(null)

// Three.js variables
let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
const cubes: THREE.Points[] = []
let selectionBox: THREE.LineSegments
let animationId: number
let raycaster: THREE.Raycaster
let mouse: THREE.Vector2
const cubeReset: boolean[] = new Array(9).fill(false)

const SPACING = 14 

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

function initThree() {
  if (!container.value) return
  scene = new THREE.Scene()
  
  const aspect = container.value.clientWidth / container.value.clientHeight
  camera = new THREE.PerspectiveCamera(35, aspect, 1, 1000)
  camera.position.set(35, -5, 85) 
  camera.lookAt(35, -14, 0)

  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
  renderer.setSize(container.value.clientWidth, container.value.clientHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  container.value.appendChild(renderer.domElement)

  const baseGeometry = new THREE.BufferGeometry()
  baseGeometry.setAttribute('position', new THREE.Float32BufferAttribute(createVertices(), 3))
  const circleTexture = createCircleTexture()
  
  const materialSmall = new THREE.PointsMaterial({
    size: 1, 
    vertexColors: true,
    transparent: true,
    opacity: 0.9,
    map: circleTexture,
    alphaMap: circleTexture,
    alphaTest: 0.1,
    sizeAttenuation: true,
    blending: THREE.AdditiveBlending
  })

  const materialGlobal = materialSmall.clone()
  materialGlobal.size = 2.5 

  for (let i = 0; i < 9; i++) {
    const geometry = baseGeometry.clone()
    const initialColors = new Uint8Array(3000).fill(26) // ~0.1 once normalized
    geometry.setAttribute('color', new THREE.Uint8BufferAttribute(initialColors, 3, true))
    
    const material = i === 0 ? materialGlobal : materialSmall
    const points = new THREE.Points(geometry, material)
    points.rotation.set(0.26, -0.785, -1.5)

    if (i === 0) {
      points.scale.set(2.3, 2.3, 2.3)
      points.position.set(SPACING, -SPACING, 0)
    } else {
      const channelIndex = i - 1 
      const col = (channelIndex % 3) + 2.6 
      const row = Math.floor(channelIndex / 3) 
      points.position.set(col * SPACING, -row * SPACING, 0)
    }
    
    points.userData = { id: i }
    scene.add(points)
    cubes.push(points)
  }

  const boxGeo = new THREE.BoxGeometry(10, 10, 10)
  const boxMat = new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.5 })
  selectionBox = new THREE.LineSegments(new THREE.EdgesGeometry(boxGeo), boxMat)
  scene.add(selectionBox)
  updateSelectionBox()

  raycaster = new THREE.Raycaster()
  mouse = new THREE.Vector2()

  animate()
}

function updateSelectionBox() {
  if (!selectionBox) return
  const target = cubes[props.channel]
  if (!target) return
  selectionBox.position.copy(target.position)
  selectionBox.scale.copy(target.scale)
  selectionBox.rotation.copy(target.rotation)
}

function animate() {
  animationId = requestAnimationFrame(animate)
  if (renderer && scene && camera) renderer.render(scene, camera)
}

function handleCanvasClick(event: MouseEvent) {
  if (!container.value) return
  const rect = container.value.getBoundingClientRect()
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1

  raycaster.setFromCamera(mouse, camera)
  const intersects = raycaster.intersectObjects(cubes)

  if (intersects.length > 0) {
    const intersect = intersects[0]
    if (intersect) {
      const target = intersect.object
      const id = target.userData.id
      container.value.dispatchEvent(new CustomEvent('cube-select', { detail: id, bubbles: true }))
    }
  }
}

function handleResize() {
  if (!container.value || !camera || !renderer) return
  const width = container.value.clientWidth
  const height = container.value.clientHeight
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}

// --- PUBLIC API called by Parent ---
// byteView holds raw uint8 RGB bytes (0-255)
function updateGeometry(byteView: Uint8Array) {
  const pixelCount = 1000
  const valuesPerPixel = 3
  const blockSize = pixelCount * valuesPerPixel

  for (let i = 0; i < 9; i++) {
    const offset = i * blockSize
    if (offset + blockSize <= byteView.length && cubes[i]) {
      const colors = byteView.subarray(offset, offset + blockSize)
      const cube = cubes[i]
      if (cube) {
        cube.geometry.setAttribute('color', new THREE.Uint8BufferAttribute(colors, 3, true))
        if (cube.geometry.attributes.color) {
          cube.geometry.attributes.color.needsUpdate = true
        }
        cubeReset[i] = false
      }
    } else if (cubes[i] && !cubeReset[i]) {
      // Only reset to black if not already reset
      const blackColors = new Uint8Array(blockSize)
      const cube = cubes[i]
      if (cube) {
        cube.geometry.setAttribute('color', new THREE.Uint8BufferAttribute(blackColors, 3, true))
        if (cube.geometry.attributes.color) {
          cube.geometry.attributes.color.needsUpdate = true
        }
        cubeReset[i] = true
      }
    }
  }
}

// Expose the method to the parent
defineExpose({ updateGeometry })

watch(() => props.channel, () => {
  updateSelectionBox()
})

onMounted(() => {
  initThree()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  cancelAnimationFrame(animationId)
  if (renderer) renderer.dispose()
  cubes.forEach(c => c.geometry.dispose())
})
</script>
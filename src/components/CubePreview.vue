<template>
  <div>
    <div
      @click="handleRotateCube"
      ref="scatterplot"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted } from 'vue'
import * as THREE from 'three'

const scatterplot = ref<HTMLDivElement | null>(null)
const geometry = ref<THREE.BufferGeometry | null>(null)
const rotateCube = ref(false)
const pointsRef = ref<THREE.Points | null>(null)

function setupScene() {
  const scene = new THREE.Scene()
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000)
  camera.position.set(7, 14.5, 11.5) 
  camera.up.set(-1, 0, 0) 
  camera.lookAt(-1, 0, 0)
  
  const renderer = new THREE.WebGLRenderer()
  renderer.setSize(500, 500)

  return { scene, camera, renderer }
}

function createVertices() {
  const vertices = []

  for (let i = 0; i < 10; i++) {
    for (let j = 0; j < 10; j++) {
      for (let k = 0; k < 10; k++) {
        vertices.push(
          i - 4.5,
          j - 4.5,
          k - 4.5
        )
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

function handleCubeData(data: any) {
  // data comes as a Uint8Array (Buffer), create a Float32 view on the buffer
  const floatView = new Float32Array(data.buffer, data.byteOffset, data.byteLength / 4)

  // Get the first 3000 floats, subarray creates a view, not a copy (very fast)
  const combinedColors = floatView.subarray(0, 3000)

  if (geometry.value) {
    geometry.value.setAttribute(
      'color',
      new THREE.Float32BufferAttribute(combinedColors, 3)
    )
  }
}

function handleRotateCube() {
  rotateCube.value = !rotateCube.value
  if (pointsRef.value) {
    pointsRef.value.rotation.y = 0
    pointsRef.value.rotation.z = 0
  }
}

onMounted(() => {
  if (!window.ipcRenderer) {
    console.error('Electron API not available')
    return
  }

  window.ipcRenderer.onCubeData(handleCubeData)

  const { scene, camera, renderer } = setupScene()

  if (scatterplot.value) {
    scatterplot.value.appendChild(renderer.domElement)
  }

  // Setup geometry
  geometry.value = new THREE.BufferGeometry()
  geometry.value.setAttribute(
    'position',
    new THREE.Float32BufferAttribute(createVertices(), 3)
  )

  const material = new THREE.PointsMaterial({
    size: 0.8,
    vertexColors: true,
    transparent: true,
    opacity: 0.9,
    map: circleTexture,
    alphaMap: circleTexture,
    alphaTest: 0.1,
    sizeAttenuation: true,
    blending: THREE.AdditiveBlending
  })
  
  const points = new THREE.Points(geometry.value, material)
  pointsRef.value = points
  scene.add(points)

  // Animation loop
  const animate = () => {
    requestAnimationFrame(animate)
    if (rotateCube.value) {
      points.rotation.y += 0.01
      points.rotation.z += 0.005
    }
    renderer.render(scene, camera)
  }
  animate()

})

onUnmounted(() => {
  window.ipcRenderer.removeWebSocketListener()
})
</script>

<style scoped>
</style>

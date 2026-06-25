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
let colorAttribute: THREE.BufferAttribute | null = null
let needsRender = true
let disposeCubeData: (() => void) | null = null

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
  // data arrives as raw uint8 RGB bytes (Buffer); view them directly
  const bytes = new Uint8Array(data.buffer, data.byteOffset, data.byteLength)

  if (colorAttribute) {
    // copy the first 3000 bytes (1000 LEDs x RGB) into the existing buffer.
    ;(colorAttribute.array as Uint8Array).set(bytes.subarray(0, 3000))
    colorAttribute.needsUpdate = true
    needsRender = true
  }
}

function handleRotateCube() {
  rotateCube.value = !rotateCube.value
  if (pointsRef.value) {
    pointsRef.value.rotation.y = 0
    pointsRef.value.rotation.z = 0
  }
  needsRender = true
}

onMounted(() => {
  if (!window.ipcRenderer) {
    console.error('Electron API not available')
    return
  }

  disposeCubeData = window.ipcRenderer.onCubeData(handleCubeData)

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

  colorAttribute = new THREE.Uint8BufferAttribute(new Uint8Array(3000), 3, true)
  colorAttribute.setUsage(THREE.DynamicDrawUsage)
  geometry.value.setAttribute('color', colorAttribute)

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

  // Animation loop: render only when something changed (new data or rotation)
  const animate = () => {
    requestAnimationFrame(animate)
    if (rotateCube.value) {
      points.rotation.y += 0.01
      points.rotation.z += 0.005
      needsRender = true
    }
    if (needsRender) {
      renderer.render(scene, camera)
      needsRender = false
    }
  }
  animate()

})

onUnmounted(() => {
  disposeCubeData?.()
})
</script>

<style scoped>
</style>

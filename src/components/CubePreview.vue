<template>
  <div>
    <div ref="scatterplot"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted } from 'vue'
import * as THREE from 'three'

const scatterplot = ref<HTMLDivElement | null>(null)
const colors = ref<number[]>([])
const geometry = ref<THREE.BufferGeometry | null>(null)

function setupScene() {
  const scene = new THREE.Scene()
  const camera = new THREE.PerspectiveCamera(75, 500 / 500, 0.1, 1000)
  camera.position.z = 15
  

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

function handleCubeData(message: any) {
  // console.log(message)
  colors.value = []
  const combinedColors = message[0]
  colors.value = combinedColors.flatMap(([r, g, b]: [number, number, number]) => [r, g, b])
  geometry.value?.setAttribute(
    'color', 
    new THREE.Float32BufferAttribute(colors.value, 3)
  )
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
    size: 0.5,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    map: circleTexture,
    alphaMap: circleTexture,
    alphaTest: 0.1,
    sizeAttenuation: true,
    blending: THREE.AdditiveBlending
  })
  
  const points = new THREE.Points(geometry.value, material)
  scene.add(points)

  // Animation loop
  const animate = () => {
    requestAnimationFrame(animate)
    points.rotation.x += 0.01
    points.rotation.y += 0.01
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

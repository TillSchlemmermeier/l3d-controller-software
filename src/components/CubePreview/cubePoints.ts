import * as THREE from 'three'

// The cube's 1000 LEDs as a 10×10×10 grid centred on the origin.
function createVertices(): number[] {
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

// A white disc, used as map and alphaMap so every point is drawn round.
// One texture can be shared by all the points of a component.
export function createCircleTexture(): THREE.Texture {
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

// One preview cube: 1000 points whose colours are the 3000 RGB bytes of a frame,
// written into colorAttr. The caller disposes geometry, material and texture.
export function createCubePoints(
  texture: THREE.Texture,
  { size, opacity, depthWrite }: { size: number; opacity: number; depthWrite: boolean }
) {
  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(createVertices(), 3))

  const colorAttr = new THREE.Uint8BufferAttribute(new Uint8Array(3000), 3, true)
  colorAttr.setUsage(THREE.DynamicDrawUsage)
  geometry.setAttribute('color', colorAttr)

  const material = new THREE.PointsMaterial({
    size,
    vertexColors: true,
    transparent: true,
    opacity,
    map: texture,
    alphaMap: texture,
    alphaTest: 0.1,
    sizeAttenuation: true,
    blending: THREE.AdditiveBlending,
    depthWrite
  })

  const points = new THREE.Points(geometry, material)
  return { points, colorAttr, geometry, material }
}

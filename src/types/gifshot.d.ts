// gifshot ships no type declarations and none exist on npm. This covers the
// one call we make: createGIF turns a list of image data URLs into a single
// animated GIF, handed back as a data URL on the callback.
declare module 'gifshot' {
  interface CreateGIFOptions {
    images: string[]
    gifWidth?: number
    gifHeight?: number
    interval?: number        // seconds between frames
    sampleInterval?: number  // pixel sampling, lower is better quality and slower
    numWorkers?: number
    repeat?: number          // 0 loops forever, -1 plays once
  }

  interface CreateGIFResult {
    error: boolean
    errorCode?: string
    errorMsg?: string
    image: string            // data:image/gif;base64,...
  }

  export function createGIF(
    options: CreateGIFOptions,
    callback: (result: CreateGIFResult) => void
  ): void
}

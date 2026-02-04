/**
 * Camera utilities for capturing photos from device camera
 */

/**
 * Opens camera and captures a photo
 * @returns {Promise<Blob>} Image blob
 */
export const capturePhotoFromCamera = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'environment',
        width: { ideal: 1280 },
        height: { ideal: 720 }
      }
    });

    return new Promise((resolve, reject) => {
      // Create video element
      const video = document.createElement('video');
      video.srcObject = stream;
      video.play();

      // Wait for video to be ready
      video.onloadedmetadata = () => {
        // Create canvas
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Draw video frame to canvas
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        // Stop stream
        stream.getTracks().forEach(track => track.stop());

        // Convert canvas to blob
        canvas.toBlob(
          blob => {
            if (blob) {
              resolve(blob);
            } else {
              reject(new Error('Failed to capture photo'));
            }
          },
          'image/jpeg',
          0.95
        );
      };

      video.onerror = () => {
        stream.getTracks().forEach(track => track.stop());
        reject(new Error('Failed to capture video'));
      };
    });
  } catch (error) {
    throw new Error(`Camera access error: ${error.message}`);
  }
};

/**
 * Checks if device supports getUserMedia API
 * @returns {boolean}
 */
export const isCameraSupported = () => {
  return !!(
    navigator.mediaDevices &&
    navigator.mediaDevices.getUserMedia
  );
};

/**
 * Converts Blob to File object
 * @param {Blob} blob
 * @param {string} fileName
 * @returns {File}
 */
export const blobToFile = (blob, fileName = 'photo.jpg') => {
  return new File([blob], fileName, { type: 'image/jpeg' });
};

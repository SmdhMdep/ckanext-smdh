document.addEventListener('DOMContentLoaded', function () {
    const uploadBtn = document.getElementById('upload-btn');
    const imageInput = document.getElementById('image-input');
    const cropModal = document.getElementById('crop-modal');
    const imageElement = document.getElementById('image');
    const cropBtn = document.getElementById('crop-btn');
    const imageUrlField = document.getElementById('field-image-url');
  
    let cropper;
  
    uploadBtn.addEventListener('click', () => {
      imageInput.click();
    });
  
    imageInput.addEventListener('change', (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          imageElement.src = e.target.result;
          cropModal.style.display = 'block';
  
          cropper = new Cropper(imageElement, {
            aspectRatio: 1,
            viewMode: 1,
            background: false,
            dragMode: 'move',
            guides: false,
            rotatable: false,
            scalable: false,
            zoomable: false,
            minCropBoxWidth: 256,
            minCropBoxHeight: 256,
          });
        };
        reader.readAsDataURL(file);
      }
    });
  
    cropBtn.addEventListener('click', () => {
      if (cropper) {
        const croppedImageDataURL = cropper.getCroppedCanvas({ width: 256, height: 256 }).toDataURL('image/png');
        imageUrlField.value = croppedImageDataURL;
        cropModal.style.display = 'none';
      }
    });
  });
  
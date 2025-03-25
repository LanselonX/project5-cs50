document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.querySelector('input[type=file]')
    const preview = document.getElementById('imagePreview')

    if(fileInput) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0]
            if(file) {
                const reader = new FileReader()
                reader.onload = function (event) {
                    preview.src = event.target.result
                    preview.style.display = 'block'
                }
                reader.readAsDataURL(file)
            } else {
                preview.style.display = 'none'
            }
        })
    }
})

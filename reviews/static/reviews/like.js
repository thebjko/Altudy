document.addEventListener('DOMContentLoaded', (x) => {
  const forms = document.querySelectorAll('#like-forms')
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  
  forms.forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault()
      const objectIdentifier = e.target.dataset.objectIdentifier
      const endpoint = '/reviews/like/'
      const data = {'objectIdentifier': objectIdentifier}
      const headers = {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
      }
      axios.post(endpoint, data, {headers}).then((r) => {
        swapText = r.data.swap_text
        const inputEl = document.getElementById(`${objectIdentifier}`)
        inputEl.value = `${swapText}`
      }).catch((error) => {
        console.log(error.response)
      })
    })
  })
})
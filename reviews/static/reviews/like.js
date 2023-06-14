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
        const i = form.querySelector('i')
        if (r.data.liked) {
          i.setAttribute('class', 'bi bi-hand-thumbs-up-fill')
          i.textContent = "코드 추천 취소"
        } else {
          i.setAttribute('class', 'bi bi-hand-thumbs-up')
          i.textContent = "코드 추천"
        }
        document.getElementById(`like-count-${objectIdentifier}`).textContent = r.data.count
      }).catch((error) => {
        console.log(error.response)
      })
    })
  })
})
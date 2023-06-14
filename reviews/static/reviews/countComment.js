document.addEventListener('DOMContentLoaded', (DOMContentLoadedEvent) => {
  document.body.addEventListener('clear-textarea', (event) => {
    document.getElementById(event.detail.textarea_id).value = ""
  })
  document.body.addEventListener('recount', (event) => {
    document.getElementById(event.detail.counter_id).textContent = event.detail.count
  })
})
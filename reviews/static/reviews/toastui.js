// ToastUI 및 제출
document.addEventListener('DOMContentLoaded', (event) => {
  const editorDiv = document.getElementById('editor');
  const FormTextArea = document.querySelector('textarea')
  const editor = new toastui.Editor({
    el: editorDiv,
    height: '500px',
    initialEditType: 'markdown',
    previewStyle: 'vertical',
    initialValue: FormTextArea.textContent,
  })
  const form = document.getElementById('form')
  form.addEventListener('submit', (e) => {
    e.preventDefault()
    FormTextArea.textContent = editor.getMarkdown()
    form.submit()
  });
});
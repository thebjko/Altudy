// ToastUI 및 제출
document.addEventListener('DOMContentLoaded', (event) => {
  const editorDiv = document.getElementById('editor');
  const FormTextArea = document.querySelector('textarea')
  const { Editor } = toastui;  
  const { codeSyntaxHighlight } = Editor.plugin;  
  const editor = new Editor({
    el: editorDiv,
    height: '500px',
    initialEditType: 'markdown',
    previewStyle: 'vertical',
    initialValue: FormTextArea.textContent,
    plugins: [codeSyntaxHighlight]
  })
  const form = document.getElementById('form')
  form.addEventListener('submit', (e) => {
    e.preventDefault()
    FormTextArea.textContent = editor.getMarkdown()
    form.submit()
  });
});
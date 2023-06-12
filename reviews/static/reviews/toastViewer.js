document.addEventListener('DOMContentLoaded', () => {
  const { Editor } = toastui;
  const { codeSyntaxHighlight } = Editor.plugin;
  const problemDescription = JSON.parse(
    document.getElementById('problem_description').textContent
  );

  const viewer = Editor.factory({
    el: document.querySelector('#viewer'),
    viewer: true,
    height: '600px',
    initialValue: problemDescription,
    plugins: [codeSyntaxHighlight]
  });
});

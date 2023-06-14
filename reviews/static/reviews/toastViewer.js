document.addEventListener('DOMContentLoaded', () => {
  const { Editor } = toastui;
  const { codeSyntaxHighlight } = Editor.plugin;
  const problemDescription = JSON.parse(
    document.getElementById('problem_description').textContent
  );

  Editor.factory({
    el: document.querySelector('#viewer'),
    viewer: true,
    height: '600px',
    initialValue: problemDescription,
    plugins: [codeSyntaxHighlight]
  });

  // 리뷰

  const reviewDescriptions = document.querySelectorAll('#reviewViewer');

  reviewDescriptions.forEach((reviewDescription) => {
    const viewer = Editor.factory({
      el: reviewDescription,
      viewer: true,
      height: '600px',
      initialValue: JSON.parse(reviewDescription.textContent),
      plugins: [codeSyntaxHighlight]
    });
  });
});
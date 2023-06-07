langBtnActive()

export function langBtnActive() {
  const languageBtns = document.querySelectorAll('.language-btn');
  const selectedLanguagesContainer = document.querySelector('.selected_languages__container');

languageBtns.forEach((btn) => {
  btn.addEventListener('click', () => {
    const clonedBtn = selectedLanguagesContainer.querySelector(`[data-lang='${btn.dataset.lang}']`);
    
    if (clonedBtn) {
      selectedLanguagesContainer.removeChild(clonedBtn);
      btn.classList.remove('selected-btn');
    } else {
      const newClonedBtn = btn.cloneNode(true);
      newClonedBtn.classList.add('language-btn-active', 'selected-btn', 'bi','bi-x');
      selectedLanguagesContainer.appendChild(newClonedBtn);

      newClonedBtn.addEventListener('click', () => {
        selectedLanguagesContainer.removeChild(newClonedBtn);
        btn.classList.remove('selected-btn');
      });
      
      btn.classList.add('selected-btn');
    }
  });
});

}

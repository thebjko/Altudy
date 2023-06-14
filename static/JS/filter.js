
const languageButtons = document.querySelectorAll('.language-btn');
const languageContainer = document.querySelector('.language__container')
const studiesContainer = document.querySelector('.cardlist__container')
const selectedLanguagesContainer = document.querySelector('.selected_languages__container');
const toggleCheckbox = document.getElementById('toggle')

languageButtons.forEach((button) => {
  button.addEventListener('click', async (e) => {
    button.classList.toggle('selected-btn');
    const selectedLangs = languageContainer.querySelectorAll('.selected-btn')
    const langs = Array.from(selectedLangs).map((v) => v.dataset.lang).join(',')
    const recruits = toggleCheckbox.checked
    const query = searchParam('query')
    const category = searchParam('category')
    try {
      const response = await fetch(`/studies/?query=${query}&lang=${langs}&recruits=${recruits}&category=${category}`);
      console.log(response);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const html = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const studies = doc.querySelector('.cardlist__container');
      studiesContainer.innerHTML = studies.innerHTML;
    } catch (error) {
      console.log(error);
    }
  });
});

selectedLanguagesContainer.addEventListener('click', async (e) => {
  const selectedLangs = languageContainer.querySelectorAll('.selected-btn')
  const langs = Array.from(selectedLangs).map((v) => v.dataset.lang).join(',')
  const recruits = toggleCheckbox.checked
  console.log(langs)
  const query = searchParam('query')
  const category = searchParam('category')
  try {
    const response = await fetch(`/studies/?query=${query}&lang=${langs}&recruits=${recruits}&category=${category}`);
    console.log(response);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const html = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const studies = doc.querySelector('.cardlist__container');
    studiesContainer.innerHTML = studies.innerHTML;
  } catch (error) {
    console.log(error);
  }
});

toggleCheckbox.addEventListener('change', async (e) => {
  const selectedLangs = languageContainer.querySelectorAll('.selected-btn')
  const langs = Array.from(selectedLangs).map((v) => v.dataset.lang).join(',');
  const recruits = toggleCheckbox.checked // 토글 on이면 true 반환
  const query = searchParam('query')
  const category = searchParam('category')
  try {
    const response = await fetch(`/studies/?query=${query}&lang=${langs}&recruits=${recruits}&category=${category}`);
    console.log(response);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const html = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const studies = doc.querySelector('.cardlist__container');
    studiesContainer.innerHTML = studies.innerHTML;
  } catch (error) {
    console.log(error);
  }
});

function searchParam(key) {
  value = new URLSearchParams(location.search).get(key)
  if(value == null) value = ''
  return value
}
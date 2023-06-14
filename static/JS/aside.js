import { probSearch } from './search.js';
import { conditionChange } from './conditionChange.js';

const asideItems = document.querySelectorAll('.aside__item');
const rightContentContainer = document.querySelector(
  '.right-content__container'
);
const currentURL = window.location.href;
let activeItem = asideItems[0];
activeItem.classList.add('active-item');

asideItems.forEach((item) => {
  item.addEventListener('click', () => {
    if (activeItem) {
      activeItem.classList.remove('active-item');
    }
    item.classList.add('active-item');
    activeItem = item;
    const contentPath = item.getAttribute('data-content');
    if (contentPath === 'mainboard') {
      window.location.href = currentURL;
    } else {
      fetch(contentPath)
        .then((response) => response.text())
        .then((content) => {
          rightContentContainer.innerHTML = content;

          if (contentPath === 'problem') {
            probSearch();
          } else if (contentPath === 'member') {
            conditionChange();
          }
        });
    }
  });
});

// profile.js

// DOM 요소들을 가져옵니다.
const profileTab = document.querySelector('.aside__container > div:nth-child(1)');
const studyTab = document.querySelector('.aside__container > div:nth-child(2)');
const codeTab = document.querySelector('.aside__container > div:nth-child(3)');
const profileSection = document.querySelector('.right_content-item__wrapper:nth-child(1)');
const studySection = document.querySelector('.right_content-item__wrapper:nth-child(2)');
const codeSection = document.querySelector('.right_content-item__wrapper:nth-child(3)');

// 처음 화면
profileSection.style.display = 'block';
studySection.style.display = 'none';
codeSection.style.display = 'none';

// 내 프로필 활성화
  profileTab.addEventListener('click', () => {
  profileTab.classList.add('active-item');
  studyTab.classList.remove('active-item');
  codeTab.classList.remove('active-item');
  profileSection.style.display = 'block';
  studySection.style.display = 'none';
  codeSection.style.display = 'none';
});

// 내 스터디 활성화
studyTab.addEventListener('click', () => {
  profileTab.classList.remove('active-item');
  studyTab.classList.add('active-item');
  codeTab.classList.remove('active-item');
  profileSection.style.display = 'none';
  studySection.style.display = 'block';
  codeSection.style.display = 'none';
});

// 내 코드 활성화
codeTab.addEventListener('click', () => {
  profileTab.classList.remove('active-item');
  studyTab.classList.remove('active-item');
  codeTab.classList.add('active-item');
  profileSection.style.display = 'none';
  studySection.style.display = 'none';
  codeSection.style.display = 'block';
});

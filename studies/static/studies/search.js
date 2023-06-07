const probSearchInput = document.querySelector('#prob-search-input')
const probSearchList = document.querySelector('#prob-search-list')
const isSolvedBtn = document.querySelector('#is-solved-btn')
let isSolvedValue = false

// 검색 결과 화면에 표시
const displayResults = (results) => {
  // 기존의 검색 결과 제거
  probSearchList.innerHTML = ''
  const ulElement = document.createElement('ul')
  /*
    ul 태그 class, id 추가
    ulElement.classList.add('my-class')
    ulElement.setAttribute('id', 'my-id')
  */

  if (results.length === 0) {
    // 검색 결과가 없는 경우
    displayNoResults()
    return
  }

  // 결과를 화면에 표시
  results.forEach((result) => {
    const liElement = document.createElement('li')
    const problemLink = document.createElement('a')
    /*
      문제 제목 담기는 li, a 태그 class, id 추가
      liElement.classList.add('my-class')
      liElement.setAttribute('id', 'my-id')
      problemLink.classList.add('my-class')
      problemLink.setAttribute('id', 'my-id')
    */

    problemLink.href = `http://127.0.0.1:8000/reviews/${result.id}/`
    problemLink.textContent = result.title;
    liElement.appendChild(problemLink)
    ulElement.appendChild(liElement)
  })
  probSearchList.appendChild(ulElement)
}


// 검색 결과가 없을 경우
const displayNoResults = () => {
  // 기존의 검색 결과 제거
  probSearchList.innerHTML = ''

  // 검색 결과가 없는 문구 생성
  const noResultsMessage = document.createElement('p')
  /*
    검색결과 안내 p 태그 class, id 추가
    noResultsMessage.classList.add('my-class')
    noResultsMessage.setAttribute('id', 'my-id')
  */
  
  noResultsMessage.textContent = '검색 결과가 없습니다.'
  probSearchList.appendChild(noResultsMessage)
};


// 초기 상태에서(input이 비어있는 경우) 모든 problems를 가져와서 표시
async function getInitialProblems(isSolved) {
  try {
    const studyId = probSearchInput.dataset.studyId;
    const response = await axios.get(`/studies/${studyId}/mainboard/problem/search`, {
      params: {
        isSolved: isSolved,
      }
    })
    const results = response.data.problems
    displayResults(results)
  } catch (error) {
    console.error(error)
  }
}

// problems를 가져와서 화면에 표시하는 함수
const getProblems = async (query, isSolved) => {
  try {
    const studyId = probSearchInput.dataset.studyId
    const response = await axios.get(`/studies/${studyId}/mainboard/problem/search`, {
      params: {
        query: query,
        isSolved: isSolved,
      }
    })
    const results = response.data.problems
    displayResults(results)
  } catch (error) {
    console.error(error)
  }
}


// input 이벤트 지연을 위한 debonce 함수
// 한글 타이핑을 빠르게 쳤을 때 마지막 input 이벤트처리가 안 되는 경우가 있어서 추가
function debounce(func, delay) {
  let timeoutId;

  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}


const handleProbSearchInput = debounce(async () => {
  const query = probSearchInput.value.trim();
  if (query) {
    try {
      await getProblems(query, isSolvedValue)
    } catch (error) {
      console.error(error)
    }
  } else {
    // 입력이 없는 경우 초기 상태로 복원
    getInitialProblems(isSolvedValue)
  }
}, 100)


const handleIsSolvedBtn = async () => {
  const query = probSearchInput.value.trim()
  if (isSolvedValue) {
    isSolvedValue = false
    isSolvedBtn.textContent = 'off'
  } else {
    isSolvedValue = true
    isSolvedBtn.textContent = 'on'
  }
  try {
    await getProblems(query, isSolvedValue)
  } catch (error) {
    console.error(error)
  }
  probSearchInput.focus()
}

probSearchInput.addEventListener('input', handleProbSearchInput)
isSolvedBtn.addEventListener('click', handleIsSolvedBtn)

// 초기 상태에서 모든 problems를 가져와서 표시
if (!isSolvedValue) {
  getInitialProblems(isSolvedValue)
}

probSearchInput.focus()
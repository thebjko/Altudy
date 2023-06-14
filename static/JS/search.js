export function probSearch () {

const probSearchInput = document.querySelector('#prob-search-input')
const probSearchList = document.querySelector('#prob-search-list')
const probToggleCheckbox = document.querySelector('.prob__toggle')


let isSolvedValue = false


// 검색 결과 화면에 표시
const displayResults = (results) => {
  // 기존의 검색 결과 제거
  probSearchList.innerHTML = ''
  const ulElement = document.createElement('ul')
  
    // ul 태그 class, id 추가
    ulElement.classList.add('problem-list')
    // ulElement.setAttribute('id', 'my-id')
  

  if (results.length === 0) {
    // 검색 결과가 없는 경우
    displayNoResults()
    return
  }

  // 결과를 화면에 표시
  results.forEach((result) => {
    const liElement = document.createElement('li')
    const problemLink = document.createElement('a')
    const problemInfo = document.createElement('div')
    const problemReviewCount = document.createElement('span')
    const problemDate = document.createElement('span')

    problemInfo.classList.add('problem-info-container')
    problemReviewCount.classList.add('bi','bi-code-square','review-count')

    // 문제 제목 담기는 li, a 태그 class, id 추가
    liElement.classList.add('problem-ele')
    liElement.setAttribute('id', 'my-id')

    // problemLink.href = `http://127.0.0.1:8000/reviews/${result.id}/`
    problemLink.href = `/reviews/${result.id}/`;
    problemLink.textContent = result.title;
    problemDate.textContent = result.createdAt.split(' ')[0];
    problemReviewCount.textContent = result.reviewCount;
    liElement.appendChild(problemLink)
    problemInfo.appendChild(problemReviewCount)
    problemInfo.appendChild(problemDate)
    liElement.append(problemInfo)
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
    console.log(results)
    displayResults(results)
    createPaginationButtons(response.data.paginator);
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
    createPaginationButtons(response.data.paginator);
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
  console.log(query)
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

const handleProbToggleCheckbox = async () => {
  const query = probSearchInput.value.trim()

  isSolvedValue = probToggleCheckbox.checked;

  try {
    await getProblems(query, isSolvedValue);
  } catch (error) {
    console.error(error);
  }

  probSearchInput.focus();
}

// 페이지네이션
const createPaginationButtons = (paginator) => {
  const paginationContainer = document.querySelector('.pagination-container');
  paginationContainer.innerHTML = '';

  // 이전 페이지 버튼 생성
  const previousButton = document.createElement('button');
  previousButton.textContent = 'Previous';
  previousButton.disabled = !paginator.hasPreviousPage;
  previousButton.addEventListener('click', () => {
    handlePaginationButtonClick(paginator.currentPage - 1);
  });
  paginationContainer.appendChild(previousButton);

  // 페이지 번호 버튼 생성
  for (let i = 1; i <= paginator.totalPages; i++) {
    const pageButton = document.createElement('button');
    pageButton.textContent = i.toString();
    pageButton.disabled = i === paginator.currentPage;
    pageButton.addEventListener('click', () => {
      handlePaginationButtonClick(i);
    });
    paginationContainer.appendChild(pageButton);
  }

  // 다음 페이지 버튼 생성
  const nextButton = document.createElement('button');
  nextButton.textContent = 'Next';
  nextButton.disabled = !paginator.hasNextPage;
  nextButton.addEventListener('click', () => {
    handlePaginationButtonClick(paginator.currentPage + 1);
  });
  paginationContainer.appendChild(nextButton);
};

// 페이지네이션 버튼 클릭 시 실행되는 함수
const handlePaginationButtonClick = (pageNumber) => {
  const studyId = probSearchInput.dataset.studyId;
  const query = probSearchInput.value.trim();
  const isSolved = probToggleCheckbox.checked;

  axios.get(`/studies/${studyId}/mainboard/problem/search`, {
    params: {
      query: query,
      isSolved: isSolved,
      page: pageNumber
    }
  })
  .then(response => {
    const results = response.data.problems;
    displayResults(results);
    createPaginationButtons(response.data.paginator);
  })
  .catch(error => {
    console.error(error);
  });
};

probSearchInput.addEventListener('input', handleProbSearchInput)
probToggleCheckbox.addEventListener('change', handleProbToggleCheckbox)

// 초기 상태에서 모든 problems를 가져와서 표시
if (!isSolvedValue) {
  getInitialProblems(isSolvedValue)
}

probSearchInput.focus()

}

function searchProblemsByTag(tag) {
  fetch(`/studies/{{ problem.study.pk }}/mainboard/problem/search?tags=${encodeURIComponent(tag)}`)
    .then(response => response.json())
    .then(data => {
      console.log(data.problems)
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
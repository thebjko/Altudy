// 비동기 Comment 수정
const commentUpdateForms = document.querySelectorAll('.comment-update-form');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

commentUpdateForms.forEach((commentUpdateForm) => {
  commentUpdateForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const studyId = e.target.dataset.studyId;
    const commentId = e.target.dataset.commentId;
    const commentField = document.getElementById(
      `comment-content-${commentId}`
    );
    const commentText = commentField.textContent;
    commentUpdateForm.hidden = true;
    const htmlStr = `
    <form class="comment-update-field-form">
      <input type="hidden" id="commentOriginalContent-${commentId}" name="originalContent" value="${commentText}">
      <textarea name="commentContent" id="commentContent-${commentId}" cols="" rows="5">${commentText}</textarea>
      <div class="comment-ud-btn__container">
      <button type="submit" id="commentUpdateConfirm-${commentId}" value="${commentId}" class="button button-small">수정</button>
      <button type="submit" class="commentCancel button button-small" id="commentCancel-${commentId}" value="${commentId}">취소</button>
      </div>
    </form>
    `;
    commentField.innerHTML = htmlStr;
    const btnCancel = document.getElementById(`commentCancel-${commentId}`);
    btnCancel.addEventListener('click', (e) => {
      e.preventDefault();
      const originalContent = document.getElementById(
        `commentOriginalContent-${commentId}`
      );

      commentField.innerHTML = originalContent.value;
      commentUpdateForm.hidden = false;
    });

    const btnUpdate = document.getElementById(
      `commentUpdateConfirm-${commentId}`
    );
    btnUpdate.addEventListener('click', (e) => {
      e.preventDefault();
      const newContent = document.getElementById(
        `commentContent-${commentId}`
      ).value;

      const params = new URLSearchParams();
      params.append('content', newContent);
      params.append('csrfmiddlewaretoken', csrftoken);
      console.log(params);
      axios
        .post(`/studies/${studyId}/comment/${commentId}/update/`, params)
        .then((response) => {
          commentField.innerHTML = response.data.content;
        })
        .catch((error) => {
          console.log(error);
        });

      commentUpdateForm.hidden = false;
    });
  });
});

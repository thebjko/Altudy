
const selectElement = document.getElementById('condition-select');
const selectedOption = selectElement.querySelector('option[selected]');
console.log(selectedOption)
if (selectedOption) {
  selectElement.prepend(selectedOption);
}

function updateAction(selectElement) {
  var form = document.getElementById('condition-form');
  var actionUrl = form.action.replace('/condition/0/', '/condition/' + selectElement.value + '/');
  form.action = actionUrl;
  form.submit();
}

// window.addEventListener('load', setDefaultOption);
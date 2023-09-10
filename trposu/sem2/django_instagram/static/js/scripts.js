function AddBsError(fieldStrId, errorMsg) {
    // fieldStrId - str, errorMsg - HTML str or None (empty str)
    let incorrectField = document.getElementById(fieldStrId);
    if (incorrectField) {
        incorrectField.classList.add("is-invalid");
        let incorrectParentDiv = incorrectField.closest("div");
        if (incorrectParentDiv) {
            incorrectParentDiv.classList.add("is-invalid");
        }
        if (errorMsg) {
            let feedbackDiv = document.createElement('div');
            feedbackDiv.className = 'invalid-feedback';
            feedbackDiv.innerHTML = errorMsg;
            incorrectParentDiv.insertAdjacentElement('afterend', feedbackDiv);
        }
    }
}
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

function changeCountText(is_add, is_zero, element) {
    let initialCount = isNaN(parseInt(element.innerText)) ? 0 : parseInt(element.innerText);
    let finalCount = is_add? initialCount + 1 : initialCount - 1;
    if (is_zero) {
        element.innerText = finalCount;
    } else {
        element.innerText = finalCount ? finalCount : "";
    }
}

function pressLike() {
    let likeElem = this;
    let postId = likeElem.parentNode.parentNode.parentNode.dataset.postId;
    let isLiked = likeElem.classList.contains('like-liked');

    $.ajax({
        type: "GET",
        url: '/ajax/like/',
        data: {
            action: isLiked ? 'remove' : 'add',
            post: postId,
        },
        success: function(response) {
            if (response.is_success) {
                let likeCountElem = likeElem.parentNode.querySelector('.like-count');
                if (isLiked) {
                    likeElem.classList.remove('like-liked');
                    changeCountText(false, false, likeCountElem);
                } else {
                    likeElem.classList.add('like-liked');
                    changeCountText(true, false, likeCountElem);
                }
            } else {
                console.error(response.message);
            }
        },
        error: function(response) {
            console.error(response);
        }
    });
}

function pressFollow() {
    let followElem = this;
    let userId = followElem.dataset.userId;
    let isFollowed = followElem.classList.contains('follow-followed');

    $.ajax({
        type: "GET",
        url: '/ajax/follow/',
        data: {
            action: isFollowed ? 'unfollow' : 'follow',
            user: userId,
        },
        success: function(response) {
            if (response.is_success) {
                let followersCountElem = document.querySelector('#followers-count');
                if (isFollowed) {
                    followElem.classList.remove('follow-followed');
                    followElem.innerText = "Подписаться";
                    changeCountText(false, true, followersCountElem);
                } else {
                    followElem.classList.add('follow-followed');
                    followElem.innerText = "Подписка";
                    changeCountText(true, true, followersCountElem);
                }
            } else {
                console.error(response.message);
            }
        },
        error: function(response) {
            console.error(response);
        }
    });
}
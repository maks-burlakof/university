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

/* AJAX */

function changeCountText(is_add, is_zero, element) {
    let initialCount = isNaN(parseInt(element.innerText)) ? 0 : parseInt(element.innerText);
    let finalCount = is_add? initialCount + 1 : initialCount - 1;
    if (element) {
        if (is_zero) {
            element.innerText = finalCount;
        } else {
            element.innerText = finalCount ? finalCount : "";
        }
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

function pressBookmark() {
    let bookmarkElem = this;
    let postId = bookmarkElem.parentNode.parentNode.parentNode.dataset.postId;
    let isMarked = bookmarkElem.classList.contains('bookmark-marked');

    $.ajax({
        type: "GET",
        url: '/ajax/bookmark/',
        data: {
            action: isMarked ? 'remove' : 'add',
            post: postId,
        },
        success: function(response) {
            if (response.is_success) {
                let bookmarkCountElem = bookmarkElem.parentNode.querySelector('.bookmark-count');
                if (isMarked) {
                    bookmarkElem.classList.remove('bookmark-marked');
                    changeCountText(false, false, bookmarkCountElem);
                } else {
                    bookmarkElem.classList.add('bookmark-marked');
                    changeCountText(true, false, bookmarkCountElem);
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

function pressCommentDelete() {
    let commentElem = this;
    let commentId = commentElem.dataset.commentId;

    $.ajax({
        type: "GET",
        url: '/ajax/comment/delete/',
        data: {
            comment: commentId,
        },
        success: function(response) {
            if (response.is_success) {
                location.reload();
            } else {
                console.error(response.message);
            }
        },
        error: function(response) {
            console.error(response);
        }
    });
}

function qrCodeGenerator(url) {
    let qrElement = document.querySelector('#share-qr');
    let qrUrlElement =document.querySelector('#share-qr-url');

    $.ajax({
        type: "GET",
        url: '/ajax/qr/',
        data: {
            text: url,
        },
        success: function(response) {
            if (response.is_success) {
                qrElement.innerHTML = `<img src="data:image/png;base64, ${response.qr_image_base64}">`;
                qrUrlElement.value = url;
            } else {
                console.error(response.message);
            }
        },
        error: function(response) {
            console.error(response);
        }
    });
}

/* POST MODALS */

$(window).on('load', function() {

    // Post modal
    let postModal = document.getElementById('post-modal');
    if (postModal) {
        postModal.addEventListener('show.bs.modal', event => {
            let postButton = event.relatedTarget;
            let postId = postButton.getAttribute('data-bs-whatever');
            let profileUsername = postButton.getAttribute('data-bs-username');
            // Go to publication
            let formPostUrl = postModal.querySelector('#post-details-url');
            formPostUrl.href = `/post/${postId}/`;
            // Share
            let formSharePost = postModal.querySelector('#post-details-share');
            formSharePost.setAttribute('data-pk', `${postId}`);
            // Go to profile
            let formProfileUrl = postModal.querySelector('#post-details-profile');
            formProfileUrl.href = `/profile/${profileUsername}/`;
            formProfileUrl.innerText = `Перейти к @${profileUsername}`;
        })
    }

    // Share modal
    let shareModal = document.getElementById('post-share-modal');
    if (shareModal) {
        shareModal.addEventListener('show.bs.modal', event => {
            let postButton = event.relatedTarget;
            let buttonType = postButton.getAttribute('data-type');
            let qrUrl = "";

            if (buttonType === "post") {
                let postId = postButton.getAttribute('data-pk');
                qrUrl = window.location.protocol + '//' + window.location.host + `/post/${postId}/`;
            } else if (buttonType === "user") {
                let userUsername = postButton.getAttribute('data-username');
                qrUrl = window.location.protocol + '//' + window.location.host + `/profile/${userUsername}/`;
            }
            qrCodeGenerator(qrUrl);
        })
    }
    $('#share-qr-copy').on('click', function() {
        let copyBtn = this;
        let qrUrl = this.parentNode.querySelector('#share-qr-url').value;

        navigator.clipboard.writeText(qrUrl);
        copyBtn.innerHTML = '<i class="fa-solid fa-check"></i>';
        setTimeout(function() {
            copyBtn.innerHTML = '<i class="fa-solid fa-link me-1"></i> Копировать';
        }, 3000);
    });
});
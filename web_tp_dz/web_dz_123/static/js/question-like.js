function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function main() {
    console.log('TEST')
    const likeElements = document.querySelectorAll('.question-like-control')
    for (const one_element of likeElements) {
        const likeButton = one_element.getElementsByClassName('like-btn')[0]
        const dislikeButton = one_element.getElementsByClassName('dislike-btn')[0]
        const count = one_element.getElementsByClassName('like-counter')[0]
        const question = one_element.dataset.questionId
        
        function likeOrDislike(isLike) {
            console.log('тык')
            const request = new Request('/like-question/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    questionId: question,
                    isLike: isLike
                })
            })

            fetch(request)
            .then((response) => response.json())
            .then((data) => {
                count.innerHTML = data.rating
            })
        }
        
        likeButton.onclick = () => likeOrDislike(true)
        dislikeButton.onclick = () => likeOrDislike(false)
    }
}

main()
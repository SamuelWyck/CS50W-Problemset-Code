document.addEventListener("DOMContentLoaded", function() {
    const follow_btn_div = document.querySelector("#follow-user-btn-div")
    generate_follow_btn(follow_btn_div)
    
    const editpost = document.querySelectorAll(".edit-post")
    editpost.forEach(function(link) {
        const post_number = link.dataset.postId
        link.onclick = function() {
            edit_post(post_number)
    }})
    let div_postid_list = []
    const like_btn_divs = document.querySelectorAll(".like-btn-div")
    like_btn_divs.forEach(function(div) {
        div_postid_list.push(div.dataset.postId)
    })
    generate_like_btns(div_postid_list, like_btn_divs)

    const user_profile_links = document.querySelectorAll(".profile-link")
    user_profile_links.forEach(function(profile_link) {
        const user_id = profile_link.dataset.userId
        profile_link.onclick = function() {
            window.location.href = `/load_profile?user_id=${user_id}`
        }
    })
})


function edit_post(post_id) {
    const content_div =  document.querySelector(`#post-${post_id}-content-div`)
    const post_content = document.querySelector(`#post-${post_id}-content`)
    const post_textarea = document.querySelector(`#post-${post_id}-textarea`)
    const save_btn_div = document.querySelector(`#post-${post_id}-save-btn-div`)
    const save_btn = document.querySelector(`#post-${post_id}-save-btn`)

    content_div.style.marginRight = "0%"
    post_content.style.display = "none"
    post_textarea.style.display = "block"
    save_btn_div.style.display = "block"

    save_btn.onclick = function() {
        if (post_textarea.value !== post_content.innerHTML) {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
        fetch("/edit_post", {
            method: "POST",
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                post_id: post_id,
                post_content: post_textarea.value
            })
        })
        .then(function(response) {
            return response.json()
        })
        .then(function(result) {
            if (result.error !== "") {
                alert(result.error)
            } else {
                post_content.innerHTML = post_textarea.value
                post_content.style.display = "block"
                content_div.style.marginRight = "5%"
                post_textarea.style.display = "none"
                save_btn_div.style.display = "none"

            }
        })
    } else {
        post_content.style.display = "block"
        content_div.style.marginRight = "5%"
        post_textarea.style.display = "none"
        save_btn_div.style.display = "none"
    }
}
}

function generate_like_btns(post_id_list, div_element_list) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const logged_in =  document.querySelector("#logged-in").value
    if (logged_in === "true") {
    fetch(`/handle_like?post_id_list=${post_id_list}`, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken
        }
    })
    .then(function(response) {
        return response.json()
    })
    .then(function(result) {
        console.log(result)
        div_element_list.forEach(function(div) {
            const btn = document.createElement("button")
            if (result[div.dataset.postId] === "false") {
                console.log("false")
                btn.className = "btn btn-sm btn-outline-primary"
                btn.innerHTML = "Like"
                btn.onclick = function() {
                    add_like(div.dataset.postId, div)
                }
                div.append(btn)
            } else {
                btn.className = "btn btn-sm btn-primary"
                btn.innerHTML = "Liked"
                btn.onclick = function() {
                    remove_like(div.dataset.postId, div)
                }
                div.append(btn)
            }
        })
    })}
}

function add_like(post_id, div) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    fetch("/handle_like", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            post_id: post_id,
            action: "add"
        })
    })
    .then(function(response) {
        return response.json()
    })
    .then(function(result) {
        console.log(result)
        const btn = document.createElement("button")
        btn.className = "btn btn-sm btn-primary"
        btn.innerHTML = "Liked"
        btn.onclick = function() {
            remove_like(div.dataset.postId, div)
        }
        div.innerHTML = ""
        div.append(btn)
        const likes_div = document.querySelector(`#post-${post_id}-likes`)
        let likes = Number(likes_div.innerHTML)
        likes++
        likes_div.innerHTML = likes
    })
}

function remove_like(post_id, div) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    fetch("/handle_like", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            post_id: post_id,
            action: "remove"
        })
    })
    .then(function(response) {
        return response.json()
    })
    .then(function(result) {
        console.log(result)
        const btn = document.createElement("button")
        btn.className = "btn btn-sm btn-outline-primary"
        btn.innerHTML = "Like"
        btn.onclick = function() {
            add_like(div.dataset.postId, div)
        }
        div.innerHTML = ""
        div.append(btn)
        const likes_div = document.querySelector(`#post-${post_id}-likes`)
        let likes = Number(likes_div.innerHTML)
        likes--
        likes_div.innerHTML = likes
    })
}

function generate_follow_btn(btn_div) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const logged_in =  document.querySelector("#logged-in").value
    const active_users_profile = document.querySelector("#active-users-profile").value
    if (logged_in === "true" && active_users_profile === "false") {
        fetch(`/handle_follow?profile_user_id=${btn_div.dataset.userId}`, {
            method: "GET",
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": csrftoken
            }
        })
        .then(function(response) {
            return response.json()
        })
        .then(function(result) {
            console.log(result)
            const btn = document.createElement("button")
            if (result.following === "false") {
                btn.className = "btn btn-outline-primary"
                btn.innerHTML = "Follow"
                btn.onclick = function(){
                    follow(btn_div)
                }
                btn_div.append(btn)
            } else {
                btn.className = "btn btn-primary"
                btn.innerHTML = "Followed"
                btn.onclick = function() {
                    unfollow(btn_div)
                }
                btn_div.append(btn)
            }
        })
    }
}

function follow(div) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    fetch("/handle_follow", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            profile_user: div.dataset.userId,
            action: "follow"
        })
    })
    .then(function(response) {
        return response.json()
    })
    .then(function(result) {
        const btn = document.createElement("button")
        btn.className = "btn btn-primary"
        btn.innerHTML = "Followed"
        btn.onclick = function() {
            unfollow(div)
        }
        div.innerHTML = ""
        div.append(btn)
        const follow_count = document.querySelector("#follower-count")
        let followers = Number(follow_count.innerHTML)
        followers++
        follow_count.innerHTML = followers
    })
}

function unfollow(div) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    fetch("/handle_follow", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            profile_user: div.dataset.userId,
            action: "unfollow"
        })
    })
    .then(function(response) {
        return response.json()
    })
    .then(function(result) {
        const btn = document.createElement("button")
        btn.className = "btn btn-outline-primary"
        btn.innerHTML = "Follow"
        btn.onclick = function() {
            follow(div)
        }
        div.innerHTML = ""
        div.append(btn)
        const follow_count = document.querySelector("#follower-count")
        let followers = Number(follow_count.innerHTML)
        followers--
        follow_count.innerHTML = followers
    })
}
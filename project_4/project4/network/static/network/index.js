document.addEventListener("DOMContentLoaded", function() {

    const logged_in =  document.querySelector("#logged-in").value
    if (logged_in === "false") {
        document.querySelector("#posts-div").style.marginTop = "2%"
    } 
    if (logged_in === "true") {
    document.querySelector("#new-post-form").onsubmit = function(event) {
        event.preventDefault()
        new_post()
    }
    document.querySelector("#hide-new-post-form").onclick = function() {
        hide_newpost_form()
    }
    document.querySelector("#show-new-post-form").onclick = function() {
        show_newpost_form()
    }}
    
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

function new_post() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    const error = document.querySelector("#error-message")
    const post_btn = document.querySelector("#submit-new-post")
    error.style.display = "none"
    post_btn.style.marginBottom = "0px"

    fetch("/new_post", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            post_user: document.querySelector("#new-post-user").value,
            post_content: document.querySelector("#new-post-content").value
        })
    })
    .then(function(response) {
        return response.json()
    })
    .then(function(result) {
        console.log(result)
        if (result.error !== "") {
            error.style.display = "block"
            error.innerHTML = result.error
            post_btn.style.marginBottom = "23px"
        } else {
            document.querySelector("#new-post-content").value = ""
            error.style.display = "none"
            error.innerHTML = ""
            post_btn.style.marginBottom = "0px"
            location.reload(true)
        }
    })
}

function show_newpost_form() {
    const new_post_form = document.querySelector("#new-post-form")
    document.querySelector("#posts-div").style.marginTop = "9%"
    document.querySelector("#error-message").innerHTML = ""
    document.querySelector("#new-post-content").value = ""
    document.querySelector("#submit-new-post").style.marginBottom = "0px"
    document.querySelector("#error-message").style.display = 'none'
    new_post_form.style.display = 'block'
    document.querySelector("#show-new-post-form").style.display = "none"
}

function hide_newpost_form() {
    const new_post_form = document.querySelector("#new-post-form")
    new_post_form.style.display = 'none'
    document.querySelector("#posts-div").style.marginTop = "2%"
    document.querySelector("#show-new-post-form").style.display = "block"
}

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

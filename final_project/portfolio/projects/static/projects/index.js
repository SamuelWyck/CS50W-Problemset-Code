document.addEventListener("DOMContentLoaded", function() {
    const project_divs = document.querySelectorAll(".col-4")
    project_divs.forEach(function(project_div) {
        project_div.onclick  = function() {
            window.location.href = `projects/project_page/${project_div.dataset.projectId}`
        }
    })
    document.querySelector("#project-link").style.display = "none"
})
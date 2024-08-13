document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector("#single-email-view").style.display = "none";
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector("form").onsubmit = function(event) {
    event.preventDefault()
    fetch("/emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value})
    })
    .then(function(response) {
      return response.json()
    })
    .then(function(result) {
      console.log(result)
      load_mailbox('sent')
    })
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector("#single-email-view").style.display = "none";

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(function(response) {
    return response.json()
  })
  .then(function(emails) {
    console.log(emails)
    emails.forEach(function(email) {
      const element = document.createElement("div")
      element.style.border = "1px solid black"
      element.style.borderRadius = "5px"
      element.style.margin = "10px"
      element.style.padding = "5px"
      element.style.cursor = "pointer"
      element.className = "container-fluid"
      //need to add an eventlistener to allow to click on the email
      if (email.read === true) {
        element.style.backgroundColor = "lightgray"
      }

      const row = document.createElement("div")
      row.className = "row align-items-center"

      const span_from = document.createElement("div")
      span_from.style.fontSize = "20px"
      span_from.style.fontWeight = "bold"
      span_from.style.margin = "10px"
      span_from.style.overflow = "hidden"
      span_from.style.whiteSpace = "nowrap"
      span_from.style.textOverflow = "ellipsis"
      span_from.className = "col-md-3"
      span_from.innerHTML = `From: ${email.sender}`
      row.append(span_from)

      const span_subject = document.createElement("div")
      span_subject.style.fontSize = "20px"
      span_subject.style.fontWeight = "bold"
      span_subject.style.margin = "10px"
      span_subject.style.overflow = "hidden"
      span_subject.style.whiteSpace = "nowrap"
      span_subject.style.textOverflow = "ellipsis"
      span_subject.className = "col"
      span_subject.innerHTML = `Subject: ${email.subject}`
      row.append(span_subject)

      const span_time = document.createElement("div")
      span_time.style.fontSize = "15px"
      span_time.style.margin = "10px"
      span_time.className = "col-md-2 offset-md-2"
      span_time.innerHTML = email.timestamp
      row.append(span_time)

      element.append(row)
      element.addEventListener("click", function() {
        view_email(email.id)
      })
      document.querySelector("#emails-view").append(element)
    })
  })
}

function view_email(email_id) {
  console.log(`email: ${email_id} was clicked`)

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector("#single-email-view").style.display = "block";

  fetch(`/emails/${email_id}`)
  .then(function(response) {
    return response.json()
  })
  .then(function(email) {
    console.log(email)

    const email_div = document.querySelector("#single-email-view")
    email_div.innerHTML = ""

    const element = document.createElement("div")
    element.className = 'container-fluid'
    element.style.border = "1px solid lightgray"
    element.style.borderRadius = "5px"
    element.style.padding = "10px"
    element.style.margin = "10px"
    element.style.cursor = "default"

    const sender = document.createElement("div")
    sender.innerHTML = email.sender
    sender.style.fontWeight = "bold"
    sender.style.marginLeft = "10px"
    element.append(sender)


    const row1 = document.createElement("div")
    row1.className = "row justify-content-end"
    element.append(row1)

    const getters = document.createElement('div')
    let text = "To: "
    email.recipients.forEach(function(email) {
      text = text.concat(`${email}, `)
    })
    let length = text.length
    text = text.slice(0, length - 2)
    getters.innerHTML = text
    getters.className = "col"
    getters.style.fontSize = "12px"
    getters.style.marginLeft = "10px"
    getters.style.overflow = "hidden"
    getters.style.whiteSpace = "nowrap"
    getters.style.textOverflow = "ellipsis"
    row1.append(getters)


    const reply_btn = document.createElement("button")
    reply_btn.innerHTML = "Reply"
    reply_btn.className = "btn btn-secondary btn-sm"
    reply_btn.style.margin = "10px"
    reply_btn.style.marginTop = "0px"
    reply_btn.addEventListener("click", function () {
      compose_reply_email(email)
    })
    row1.append(reply_btn)


    const user_email = document.querySelector("#user_email").innerHTML

    if (email.sender != user_email) {
    const archive_btn = document.createElement("button")
    if (email.archived === false) {
      archive_btn.innerHTML = "Archive"
      archive_btn.className = "btn btn-secondary btn-sm"
      archive_btn.addEventListener("click", function() {
        archive_email(email_id, true)
      })
    } else {
      archive_btn.innerHTML = "Archived"
      archive_btn.className = "btn btn-outline-secondary btn-sm"
      archive_btn.addEventListener("click", function() {
        archive_email(email_id, false)
      })
    }
    archive_btn.style.margin = "10px"
    archive_btn.style.marginTop = "0px"
    archive_btn.style.marginRight = "50px"
    row1.append(archive_btn) } else {
      reply_btn.style.marginRight = "5%"
    }

    const row2 = document.createElement("div")
    row2.className = "row justify-content-end"
    row2.style.borderBottom = "1px solid lightgray"
    row2.style.marginLeft = "5px"
    row2.style.marginRight = "5px"
    element.append(row2) 


    const header  = document.createElement("div")
    header.className = "col-md-8"
    header.style.fontWeight = "bold"
    header.style.fontSize = "25px"
    header.style.overflow = "hidden"
    header.style.whiteSpace = "nowrap"
    header.style.textOverflow = "ellipsis"
    header.innerHTML = email.subject
    row2.append(header)

    const time_stamp = document.createElement("div")
    time_stamp.className = "col align-self-center offset-md-2"
    time_stamp.innerHTML = email.timestamp
    time_stamp.style.fontSize = "13px"
    row2.append(time_stamp)

    const body = document.createElement("div")
    body.innerHTML = email.body
    body.className = "text-wrap text-break"
    body.style.margin = "10px"
    body.style.padding = "5px"
    element.append(body)

    email_div.append(element)

  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true
    })
  })
  })
}
function archive_email(email_id, bool) {
  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: bool
    })
  })
  .then(function() {
    load_mailbox("inbox")
  })
}

function compose_reply_email(email) {
  //console.log(email)

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector("#single-email-view").style.display = "none";
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-recipients').value = email.sender

  let text = email.subject.slice(0, 3)
  if (text === "Re:") {
    document.querySelector("#compose-subject").value = email.subject
  } else {
    document.querySelector("#compose-subject").value = `Re: ${email.subject}`
  }

  const body_text = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`

  document.querySelector("#compose-body").value = body_text

  document.querySelector("form").onsubmit = function(event) {
    event.preventDefault()
    fetch("/emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value})
    })
    .then(function(response) {
      return response.json()
    })
    .then(function(result) {
      console.log(result)
      load_mailbox('sent')
    })
  }
}
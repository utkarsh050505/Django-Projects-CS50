document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#submit').addEventListener('click', () => send_mail(event))

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);

    let inbox = [];
    let sent = [];

    for (let i = 0; i < emails.length; i++) {
      if (emails[i]['sender'] == document.querySelector("#sender").value) {
        sent.push(emails[i]);
      } else if (emails[i]['recipients'] == document.querySelector("#sender").value) {
        inbox.push(emails[i]);
      }
    }

    for (let i = 0; i < sent.length; i++) {
      const element = createEmailCard(sent[i], 'to');
      document.querySelector('#emails-view').append(element);
    }

    for (let i = 0; i < inbox.length; i++) {
      const element = createEmailCard(inbox[i], 'from');
      document.querySelector('#emails-view').append(element);
    }
  });

  function createEmailCard(email, x) {
    const element = document.createElement('div');
    element.className = 'card';
    element.style.padding = '1rem';
    element.style.marginBottom = '10px';
    element.style.border = '1px solid #ccc';
    element.style.borderRadius = '8px';
    element.style.cursor = 'pointer';
    element.style.display = 'flex';
    element.style.flexDirection = 'row';
    element.style.justifyContent = 'space-between';

    const sender = email['sender']
    const reciever = email['recipients']

    if (x == 'to') {
    element.innerHTML = `
      <div style="font-weight: bold;">${x}: ${reciever}</div>
      <div> ${email['subject']}</div>
      <div> ${email['timestamp']}</div>
    `;
    }
    else if (x == 'from' && email['read'] == true) {
      element.style.background = '#D0D0D0'
      element.innerHTML = `
      <div style="font-weight: bold;">${x}: ${email['sender']}</div>
      <div> ${email['subject']}</div>
      <div> ${email['timestamp']}</div>
    `;
    }
    else {
      element.innerHTML = `
      <div style="font-weight: bold;">${x}: ${email['sender']}</div>
      <div> ${email['subject']}</div>
      <div> ${email['timestamp']}</div>
    `;
    }

    element.addEventListener('click', function() {
      const emailsView = document.querySelector('#emails-view');
      emailsView.innerHTML = '';

      if (email['archived'] === false && x == 'from') {
        emailsView.innerHTML = `
          <div>
            <p><strong>From:</strong> ${email['sender']}</p>
            <p><strong>To:</strong> ${email['recipients']}</p>
            <p><strong>Subject:</strong> ${email['subject']}</p>
            <p><strong>Timestamp:</strong> ${email['timestamp']}</p>
            <input type='submit' value='Reply' id='reply'>
            <hr>
            <p>${email['body']}</p>
          </div>
          <br>
          <input type='submit' name='arch' value='Archive' id='archive' class='btn btn-primary'>
        `;
      } else if (email['archived'] === true && x == 'from') {
        emailsView.innerHTML = `
          <div>
            <p><strong>From:</strong> ${email['sender']}</p>
            <p><strong>To:</strong> ${email['recipients']}</p>
            <p><strong>Subject:</strong> ${email['subject']}</p>
            <p><strong>Timestamp:</strong> ${email['timestamp']}</p>
            <input type='submit' value='Reply' id='reply'>
            <hr>
            <p>${email['body']}</p>
          </div>
          <br>
          <input type='submit' name="arch" value='Unarchive' id='unarchive' class='btn btn-primary'>
        `;
      } else if (email['archived'] === true && x == 'to') {
        emailsView.innerHTML = `
          <div>
            <p><strong>From:</strong> ${email['sender']}</p>
            <p><strong>To:</strong> ${email['recipients']}</p>
            <p><strong>Subject:</strong> ${email['subject']}</p>
            <p><strong>Timestamp:</strong> ${email['timestamp']}</p>
            <hr>
            <p>${email['body']}</p>
          </div>
          <br>
          <input type='submit' name="arch" value='Unarchive' id='unarchive' class='btn btn-primary'>
        `;
      } else if (email['archived'] === false && x == 'to') {
        emailsView.innerHTML = `
          <div>
            <p><strong>From:</strong> ${email['sender']}</p>
            <p><strong>To:</strong> ${email['recipients']}</p>
            <p><strong>Subject:</strong> ${email['subject']}</p>
            <p><strong>Timestamp:</strong> ${email['timestamp']}</p>
            <hr>
            <p>${email['body']}</p>
          </div>
          <br>
          <input type='submit' name="arch" value='Archive' id='archive' class='btn btn-primary'>
        `;
      }

      const replyButton = document.querySelector('#reply');

      if (replyButton) {
        replyButton.addEventListener('click', () => reply(email));
      }

      const archiveButton = document.querySelector('#archive');
      const unarchiveButton = document.querySelector('#unarchive');

      if (archiveButton) {
        archiveButton.addEventListener('click', () => saved(email));
      } else if (unarchiveButton) {
        unarchiveButton.addEventListener('click', () => unsaved(email));
      }

      fetch(`emails/${email['id']}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      });
    });


    return element;
  }
}

function send_mail(event) {
    event.preventDefault();

    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);

        load_mailbox('sent')
    });
}

function saved(mail) {

  fetch(`emails/${mail['id']}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  });

  load_mailbox('archive')
}

function unsaved(mail) {

  fetch(`emails/${mail['id']}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  });

  load_mailbox('inbox')
}

function reply(mail) {
  fetch(`emails/${mail['id']}`)
  .then(response => response.json())
  .then(email => {

    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';


    document.querySelector('#compose-recipients').value = `${email['sender']}`;
    document.querySelector('#compose-subject').value = `Re: ${email['subject']}`;
    document.querySelector('#compose-body').value = `



    -------------
    On ${email['timestamp']} ${email['sender']} wrote:

    ${email['body']}
    `;

  });
}

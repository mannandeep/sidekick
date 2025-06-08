async function sendMessage() {
  const input = document.getElementById("input").value;
  const responseDiv = document.getElementById("response");

  // Show loading
  responseDiv.innerHTML = "<div class='chat-bubble'>🤖 Thinking...</div>";

  const response = await fetch("http://localhost:5000/sidekick", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ notes: input })
  });

  const data = await response.json();
  const result = data.result;

  responseDiv.innerHTML = data.result.map(item => `
  <div class="chat-bubble ai">
    <strong>${item.ticket_type}:</strong> ${item.title}<br>
    <em>${item.description}</em>
  </div>
`).join('');

}

async function connectJira() {
  const url = prompt("Jira URL (e.g. https://your.atlassian.net)");
  const email = prompt("Email");
  const token = prompt("API Token");
  if (!url || !email || !token) {
    alert("Missing information");
    return;
  }
  const domain = url.replace(/^https?:\/\//, "");
  await fetch("http://localhost:5000/connect_jira", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, email, api_token: token, domain })
  });
  alert("Jira connected");
}

function formatResult(result) {
  if (result.includes("http")) {
    return result.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');
  }
  return result;
}

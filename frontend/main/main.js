async function sendMessage() {
  const input = document.getElementById("input").value;
  const responseDiv = document.getElementById("response");

  // Show loading
  responseDiv.innerHTML = "<div class='chat-bubble'>🤖 Thinking...</div>";

  const response = await fetch("http://localhost:5000/parse_notes", {
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

function formatResult(result) {
  if (result.includes("http")) {
    return result.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');
  }
  return result;
}

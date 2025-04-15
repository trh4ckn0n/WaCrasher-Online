let generatedUrl = "";

function send() {
  const phone = document.getElementById("phone").value;
  const threads = document.getElementById("threads").value;
  if (!phone) return alert("Numéro requis !");
  fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone, threads })
  })
    .then(r => r.json())
    .then(d => {
      generatedUrl = d.url;
      document.getElementById("status").innerText = "Message envoyé en boucle !";
      document.getElementById("result").innerHTML = `<a href="${d.url}" target="_blank">${d.url}</a>`;
    });
}

function shorten() {
  const phone = document.getElementById("phone").value;
  if (!phone) return alert("Numéro requis !");
  fetch("/shorten", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone })
  })
    .then(r => r.json())
    .then(d => {
      if (d.short_url) {
        generatedUrl = d.short_url;
        document.getElementById("result").innerHTML = `<a href="${d.short_url}" target="_blank">${d.short_url}</a>`;
      } else {
        alert("Erreur : " + d.error);
      }
    });
}

function getQR() {
  const phone = document.getElementById("phone").value;
  if (!phone) return alert("Numéro requis !");
  fetch("/qr", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone })
  })
    .then(r => r.json())
    .then(d => {
      generatedUrl = d.wa_url;
      const img = document.getElementById("qrimg");
      img.src = d.qr;
      img.style.display = "block";
      document.getElementById("result").innerHTML = `<a href="${d.wa_url}" target="_blank">${d.wa_url}</a>`;
    });
}

function copyLink() {
  if (!generatedUrl) return alert("Aucun lien généré !");
  navigator.clipboard.writeText(generatedUrl).then(() => {
    alert("Lien copié !");
  });
}

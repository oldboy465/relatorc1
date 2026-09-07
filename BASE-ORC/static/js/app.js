document.addEventListener("DOMContentLoaded", () => {
  const baseSelect = document.getElementById("baseSelect");
  const btnSync = document.getElementById("btnSync");
  const btnAsk = document.getElementById("btnAsk");
  const promptInput = document.getElementById("promptInput");
  const loading = document.getElementById("loading");
  const responseArea = document.getElementById("responseArea");
  const responseText = document.getElementById("responseText");
  const sourcesList = document.getElementById("sourcesList");

  const statTotal = document.getElementById("statTotal");
  const statIndexados = document.getElementById("statIndexados");
  const statData = document.getElementById("statData");

  async function loadBaseStats() {
    const baseId = baseSelect.value;
    if (!baseId) return;

    try {
      const res = await fetch(`/api/base/${baseId}/stats`);
      const data = await res.json();
      if (res.ok) {
        statTotal.textContent = data.total_documentos;
        statIndexados.textContent = data.indexados;
        statData.textContent = data.sincronizado_em || "Nunca";
      }
    } catch (err) {
      console.error("Erro ao carregar estatísticas da base:", err);
    }
  }

  btnSync.addEventListener("click", async () => {
    const baseId = baseSelect.value;
    if (!baseId) return;

    btnSync.disabled = true;
    btnSync.textContent = "⏳ Sincronizando...";

    try {
      const res = await fetch(`/api/sync/${baseId}`, { method: "POST" });
      const data = await res.json();
      if (data.success) {
        alert(`Sincronização finalizada!\nNovos: ${data.resultado.novos}\nAtualizados: ${data.resultado.atualizados}\nInalterados: ${data.resultado.inalterados}\nRemovidos: ${data.resultado.removidos}`);
        await loadBaseStats();
      } else {
        alert("Erro na sincronização: " + (data.error || "Falha desconhecida"));
      }
    } catch (err) {
      alert("Erro na requisição: " + err.message);
    } finally {
      btnSync.disabled = false;
      btnSync.textContent = "🔄 Sincronizar Base";
    }
  });

  btnAsk.addEventListener("click", async () => {
    const baseId = baseSelect.value;
    const prompt = promptInput.value.trim();

    if (!prompt) {
      alert("Por favor, digite uma pergunta.");
      return;
    }

    loading.classList.remove("hidden");
    responseArea.classList.add("hidden");
    btnAsk.disabled = true;

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ base_id: baseId, prompt: prompt })
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Erro no processamento da consulta.");
      }

      responseText.textContent = data.resposta;
      sourcesList.innerHTML = "";

      if (data.fontes && data.fontes.length > 0) {
        data.fontes.forEach(fonte => {
          const li = document.createElement("li");
          li.className = "bg-slate-800 text-slate-300 text-xs px-3 py-1.5 rounded-full border border-slate-700 flex items-center gap-1.5";
          li.innerHTML = `📄 <span>${fonte}</span>`;
          sourcesList.appendChild(li);
        });
      } else {
        sourcesList.innerHTML = `<li class="text-xs text-slate-500 italic">Nenhuma fonte vinculada diretamente.</li>`;
      }

      responseArea.classList.remove("hidden");
    } catch (err) {
      alert("Falha na consulta: " + err.message);
    } finally {
      loading.classList.add("hidden");
      btnAsk.disabled = false;
    }
  });

  baseSelect.addEventListener("change", loadBaseStats);
  loadBaseStats();
});
async function sendPrompt() {
  const prompt = document.getElementById("prompt").value.trim();
  const btnGenerar = document.getElementById("btnGenerar");
  const loading = document.getElementById("loading");
  const statusText = document.getElementById("statusText");
  
  if (!prompt) {
    return alert("Por favor escribe una orden antes de enviar.");
  }

  // Mostrar indicador de carga con mensaje
  btnGenerar.disabled = true;
  loading.style.display = "block";
  if (statusText) {
    statusText.textContent = "Analizando solicitud...";
  }

  try {
    // Simular progreso
    setTimeout(() => {
      if (statusText) statusText.textContent = "Generando estructura del reporte...";
    }, 1000);
    
    setTimeout(() => {
      if (statusText) statusText.textContent = "Creando gráficas y análisis...";
    }, 3000);

    const res = await fetch("/api/ai_agent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });

    if (res.ok) {
      if (statusText) statusText.textContent = "¡Descargando reporte!";
      
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `reporte_${Date.now()}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
      
      // Mensaje de éxito
      setTimeout(() => {
        if (statusText) {
          statusText.textContent = "✓ Reporte generado exitosamente";
          statusText.style.color = "#28a745";
        }
        setTimeout(() => {
          if (statusText) {
            statusText.textContent = "";
            statusText.style.color = "";
          }
        }, 3000);
      }, 500);
      
    } else {
      const error = await res.text();
      alert(`Error al generar el reporte: ${error}`);
      if (statusText) statusText.textContent = "";
    }
  } catch (error) {
    alert("Error de conexión. Intenta nuevamente.");
    console.error(error);
    if (statusText) statusText.textContent = "";
  } finally {
    btnGenerar.disabled = false;
    loading.style.display = "none";
  }
}
function toggleAnonimo(checkbox) {
  const campos = document.getElementById('campos-identificacao');
  const funcionario  = document.querySelector('[name="funcionario"]');
  const departamento = document.querySelector('[name="departamento"]');
  if (checkbox.checked) {
    campos.classList.add('oculto');
    if (funcionario)  funcionario.required  = false;
    if (departamento) departamento.required = false;
  } else {
    campos.classList.remove('oculto');
    if (funcionario)  funcionario.required  = true;
    if (departamento) departamento.required = true;
  }
}

async function atualizarStatus(selectEl) {
  event.preventDefault();
  const id     = selectEl.dataset.id;
  const status = selectEl.value;
  try {
    const res  = await fetch(`/atualizar_status/${id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    });
    const data = await res.json();
    if (data.sucesso) {
      selectEl.className = 'status-select status-' + status.toLowerCase().replace(/ /g, '_');
      mostrarToast(`Status: "${status}"`, 'sucesso');
    }
  } catch (e) {
    mostrarToast('Falha na conexao.', 'erro');
  }
}

function mostrarToast(mensagem, tipo = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${tipo}`;
  toast.textContent = mensagem;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('toast-show'));
  setTimeout(() => {
    toast.classList.remove('toast-show');
    toast.addEventListener('transitionend', () => toast.remove());
  }, 2800);
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .4s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });

  const anonimo = document.getElementById('anonimo');
  if (anonimo && anonimo.checked) toggleAnonimo(anonimo);
});

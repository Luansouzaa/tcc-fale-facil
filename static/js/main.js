/* ══════════════════════════════════════════
   FeedbackHub — main.js
   ══════════════════════════════════════════ */

/**
 * Mostra/oculta campos de identificação quando anônimo é marcado.
 */
function toggleAnonimo(checkbox) {
  const campos = document.getElementById('campos-identificacao');
  const funcionario = document.getElementById('funcionario');
  const departamento = document.getElementById('departamento');

  if (checkbox.checked) {
    campos.classList.add('oculto');
    funcionario.required = false;
    departamento.required = false;
  } else {
    campos.classList.remove('oculto');
    funcionario.required = true;
    departamento.required = true;
  }
}

// Inicializa o estado correto ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
  const anonimo = document.getElementById('anonimo');
  if (anonimo && anonimo.checked) toggleAnonimo(anonimo);
});

/**
 * Atualiza o status de um feedback via AJAX
 * chamado pelo onchange do <select> no card.
 */
async function atualizarStatus(selectEl) {
  const id     = selectEl.dataset.id;
  const status = selectEl.value;

  try {
    const res = await fetch(`/atualizar_status/${id}`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ status })
    });

    const data = await res.json();

    if (data.sucesso) {
      // Atualiza a classe visual do select
      selectEl.className = 'status-select status-' +
        status.toLowerCase().replace(/ /g, '_').replace('á', 'a');

      mostrarToast(`Status atualizado para "${status}"`, 'sucesso');
    } else {
      mostrarToast('Erro ao atualizar status.', 'erro');
    }
  } catch (err) {
    mostrarToast('Falha na conexão.', 'erro');
    console.error(err);
  }
}

/**
 * Exibe um toast temporário no canto da tela.
 */
function mostrarToast(mensagem, tipo = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${tipo}`;
  toast.textContent = mensagem;
  document.body.appendChild(toast);

  // Força reflow para ativar a animação de entrada
  requestAnimationFrame(() => toast.classList.add('toast-show'));

  setTimeout(() => {
    toast.classList.remove('toast-show');
    toast.addEventListener('transitionend', () => toast.remove());
  }, 2800);
}

/**
 * Auto-fecha mensagens flash após 4 segundos.
 */
document.addEventListener('DOMContentLoaded', () => {
  const flashItems = document.querySelectorAll('.flash');
  flashItems.forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .4s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });
});

function verificarParImpar() {
  const numero = document.getElementById("numero").value;

  if (numero % 2 === 0) {
    document.getElementById("resultado").textContent = `${numero} é um número PAR.`;
  } else {
    document.getElementById("resultado").textContent = `${numero} é um número ÍMPAR.`;
  }
}

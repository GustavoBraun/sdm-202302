function calcularPesoIdeal() {
  var altura = parseFloat(document.getElementById('altura').value);
  var sexo = document.getElementById('sexo').value;
  var resultadoElement = document.getElementById('resultado');

  if (altura && sexo) {
    var pesoIdeal;
    if (sexo === 'homem') {
      pesoIdeal = (72.7 * altura) - 58;
    } else {
      pesoIdeal = (62.1 * altura) - 44.7;
    }

    resultadoElement.textContent = pesoIdeal.toFixed(2);
  } else {
    resultadoElement.textContent = 'Preencha altura e sexo.';
  }
}

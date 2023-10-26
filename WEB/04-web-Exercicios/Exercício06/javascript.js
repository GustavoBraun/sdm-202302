function calcularValor() {
  var preco = parseFloat(document.getElementById('preco').value);
  var condicao = parseInt(document.getElementById('condicao').value);
  var resultadoElement = document.getElementById('resultado');

  if (preco && condicao) {
    var valorFinal;
    switch (condicao) {
      case 1:
        valorFinal = preco * 0.9; // À vista, em dinheiro ou PIX, 10% de desconto
        break;
      case 2:
        valorFinal = preco * 0.95; // À vista, no cartão de crédito, 5% de desconto
        break;
      case 3:
        valorFinal = preco; // Em duas vezes, preço normal de etiqueta sem juros
        break;
      case 4:
        valorFinal = preco * 1.06; // Em três vezes, preço normal de etiqueta mais juros de 6%
        break;
      default:
        valorFinal = preco;
    }

    resultadoElement.textContent = valorFinal.toFixed(2);
  } else {
    resultadoElement.textContent = 'Preencha o preço e escolha a condição de pagamento.';
  }
}

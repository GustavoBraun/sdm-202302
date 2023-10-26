function ordenarNumeros() {
  var num1 = parseInt(document.getElementById('num1').value);
  var num2 = parseInt(document.getElementById('num2').value);
  var num3 = parseInt(document.getElementById('num3').value);

  var numeros = [num1, num2, num3];
  numeros.sort(function (a, b) {
    return b - a;
  });

  document.getElementById('resultado').innerText = numeros.join(', ');
}
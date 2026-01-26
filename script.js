const text = document.getElementById('text-typing');
const message = 'Hola buenas esto es una prueba para hacer primero la lógica para poder teclear y luego integro la IA';
const input = document.getElementById('inputTyping');
const arrayCaracteres = []
const arrayUsuario = []

for (const letra of message) {
    const caracter = document.createElement('span');
    caracter.textContent = letra;
    arrayCaracteres.push(letra);
    text.appendChild(caracter);
}

input.addEventListener('blur', () => {
    input.focus();
});

input.addEventListener('keydown', (event) => {
    if (event.key != 'Backspace' && event.key != 'CapsLock')
    arrayUsuario.push(event.key);
    console.log(arrayUsuario);
    console.log(arrayCaracteres);
    if (event.key == 'Backspace') {
        retroceder();
    }

    comprobar()
});

function retroceder() {
    let lastIndex = arrayUsuario.length - 1;
    arrayUsuario.pop();

    text.children[lastIndex].classList.remove('correcto');
    text.children[lastIndex].classList.remove('error');


}




function comprobar() {
    for (let i = 0; i < arrayUsuario.length; i++) {
        if (arrayUsuario[i] === arrayCaracteres[i]) {
            text.children[i].classList.add('correcto');
        } else {
              text.children[i].classList.add('error');
        }
        
    }
}
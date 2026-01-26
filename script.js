const text = document.getElementById('text-typing');
let message = '';
const input = document.getElementById('inputTyping');
let arrayCaracteres = [];
let arrayUsuario = [];

const obtenerFrase = async () => {

    try {

       const response = await fetch('http://127.0.0.1:8000/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ llave: "valor" })
        });

        const data = await response.json()
        console.log(data)
        return data['respuesta']

    } catch {
        console.log('La conexión de la API fue erronea');
        message = 'Mensaje por defecto para que el usuario haga typing';
    }
}

const init = async () => {
    
    arrayCaracteres = [];
    arrayUsuario = [];
    text.innerHTML = '<h2>Generando frase...</h2>';
    message = await obtenerFrase();
    text.innerHTML = "";
        
        for (const letra of message) {
            const caracter = document.createElement('span');
            caracter.textContent = letra;
            arrayCaracteres.push(letra);
            text.appendChild(caracter);
        } 
    
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
    console.log(arrayUsuario.length)
     console.log(arrayCaracteres.length)
    if (arrayUsuario.length == arrayCaracteres.length) {
        init();
    }

    for (let i = 0; i < arrayUsuario.length; i++) {
        if (arrayUsuario[i] === arrayCaracteres[i]) {
            text.children[i].classList.add('correcto');
        } else {
              text.children[i].classList.add('error');
        }
        
    }
}

init()
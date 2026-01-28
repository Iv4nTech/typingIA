const text = document.getElementById('text-typing');
let message = '';
const input = document.getElementById('inputTyping');
let arrayCaracteres = [];
let arrayUsuario = [];
let arrayTeclasError = [];
let auxSalidaError = '';

const obtenerFrase = async () => {

    try {

       const response = await fetch('http://127.0.0.1:8000', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'errors': arrayTeclasError })
        });

        arrayTeclasError = [];
        document.getElementById('keyerror').innerHTML = "";

        const data = await response.json();
        console.log(data);
        return data['respuesta'];

    } catch {
        console.log('La conexión de la API fue erronea');
        message = 'Mensaje por defecto para que el usuario haga typing';
        return message;
    }
};

const init = async () => {
    input.disabled = true;
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

    input.disabled = false;
    input.focus()
};

input.addEventListener('blur', () => {
    input.focus();
});

input.addEventListener('keydown', (event) => {
    if (event.key != 'Backspace' && event.key != 'CapsLock') {
        arrayUsuario.push(event.key);
    }
    
    console.log(arrayUsuario);
    console.log(arrayCaracteres);
    
    if (event.key == 'Backspace') {
        retroceder();
    }

    comprobar();
});

function retroceder() {
    let lastIndex = arrayUsuario.length - 1;
    arrayUsuario.pop();

    text.children[lastIndex].classList.remove('correcto');
    text.children[lastIndex].classList.remove('error');
}

function comprobar() {
    console.log(arrayUsuario.length);
    console.log(arrayCaracteres.length);
    
    
    for (let i = 0; i < arrayUsuario.length; i++) {
        if (arrayUsuario[i] === arrayCaracteres[i]) {
            text.children[i].classList.add('correcto');
        } else {
            text.children[i].classList.add('error');
            if(!arrayTeclasError.includes(text.children[i].textContent)) {
                arrayTeclasError.push(text.children[i].textContent); 
                for (const tecla of arrayTeclasError) {
                    auxSalidaError += tecla;
                }
                document.getElementById('keyerror').innerHTML = auxSalidaError;
                auxSalidaError = "";
            }
        }
    }
    
    if (arrayUsuario.length == arrayCaracteres.length) {
        init();
    }
}

init();
let streamActual = null;
let numero1 = 0, numero2 = 0;

function procesarImagen() {
    const input = document.getElementById("imagen");
    if (!input.files.length) {
        alert("Selecciona una imagen.");
        return;
    }

    const formData = new FormData();
    formData.append("imagen", input.files[0]);

    const reader = new FileReader();
reader.onload = function (e) {
    const img = document.getElementById("preview");
    img.src = e.target.result;
    img.style.display = "block";
};
reader.readAsDataURL(input.files[0]);


    fetch("http://localhost:5000/procesar", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            numero1 = data.numero1;
            numero2 = data.numero2;
            document.getElementById("numeros").innerText = `Números detectados: ${numero1} - ${numero2}`;
            document.getElementById("opciones").style.display = "block";
        }
    })
    .catch(err => alert("Error al procesar la imagen."));
}

function realizarOperacion() {
    const op = document.getElementById("operacion").value;
    fetch("http://localhost:5000/operar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ a: numero1, b: numero2, op: op })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("resultado").innerText = data.resultado;
    })
    .catch(err => alert("Error al calcular."));
}

async function abrirCamara() {
    const select = document.getElementById("lista-camaras");
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");

    // Detectar dispositivos de video
    const dispositivos = await navigator.mediaDevices.enumerateDevices();
    const cams = dispositivos.filter(d => d.kind === "videoinput");

    // Poblar el dropdown
    select.innerHTML = "";
    cams.forEach((cam, i) => {
        const option = document.createElement("option");
        option.value = cam.deviceId;
        option.text = cam.label || `Cámara ${i + 1}`;
        select.appendChild(option);
    });

    select.onchange = () => iniciarCamara(select.value);
    iniciarCamara(cams[0].deviceId); // Iniciar con la primera cámara
    video.style.display = "block";
}


//webcam
async function abrirCamara() {
    const select = document.getElementById("lista-camaras");
    const video = document.getElementById("video");
    const btnCapturar = document.getElementById("btnCapturar");

    // Mostrar elementos
    video.style.display = "block";
    btnCapturar.style.display = "inline-block";

    // Detectar cámaras
    const dispositivos = await navigator.mediaDevices.enumerateDevices();
    const cams = dispositivos.filter(d => d.kind === "videoinput");

    select.innerHTML = "";
    cams.forEach((cam, i) => {
        const option = document.createElement("option");
        option.value = cam.deviceId;
        option.text = cam.label || `Cámara ${i + 1}`;
        select.appendChild(option);
    });

    select.onchange = () => iniciarCamara(select.value);
    iniciarCamara(cams[0].deviceId); // usar la primera cámara por defecto
}

function iniciarCamara(deviceId) {
    const video = document.getElementById("video");

    if (streamActual) {
        streamActual.getTracks().forEach(track => track.stop());
    }

    navigator.mediaDevices.getUserMedia({ video: { deviceId } })
    .then(stream => {
        streamActual = stream;
        video.srcObject = stream;
    });
}

function capturarDesdeCamara() {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const preview = document.getElementById("preview");

    const context = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);

    // Detener cámara
    streamActual.getTracks().forEach(track => track.stop());
    document.getElementById("video").style.display = "none";
    document.getElementById("btnCapturar").style.display = "none";

    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append("imagen", blob, "captura.png");

        fetch("http://localhost:5000/procesar", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                preview.src = URL.createObjectURL(blob);
                preview.style.display = "block";
                numero1 = data.numero1;
                numero2 = data.numero2;
                document.getElementById("numeros").innerText = `Números detectados: ${numero1} - ${numero2}`;
                document.getElementById("opciones").style.display = "block";
            }
        });
    });
}

//reinicio
function reiniciarTodo() {
    numero1 = 0;
    numero2 = 0;

    document.getElementById("imagen").value = "";
    document.getElementById("preview").style.display = "none";
    document.getElementById("video").style.display = "none";
    document.getElementById("btnCapturar").style.display = "none";
    document.getElementById("lista-camaras").innerHTML = "";

    document.getElementById("numeros").innerText = "Números detectados: ---";
    document.getElementById("resultado").innerText = "";
    document.getElementById("opciones").style.display = "none";
}

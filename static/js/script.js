// script.js - Página principal

const form = document.getElementById('biometricForm');
const messageDiv = document.getElementById('message');

// Función para mostrar mensajes
function showMessage(message, isSuccess = true) {
    messageDiv.textContent = message;
    messageDiv.className = `message ${isSuccess ? 'success' : 'error'}`;
    
    setTimeout(() => {
        messageDiv.className = 'message';
    }, 5000);
}

// Enviar formulario
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        state: document.getElementById('state').value,
        breathing_rate: parseInt(document.getElementById('breathing_rate').value),
        heart_rate: parseInt(document.getElementById('heart_rate').value),
        movement: parseInt(document.getElementById('movement').value),
        stress_level: document.getElementById('stress_level').value
    };

    try {
        const response = await fetch('/api/biometric-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            showMessage('✅ Datos guardados correctamente', true);
            form.reset();
            updateStats();
        } else {
            const error = await response.json();
            showMessage(`❌ Error: ${error.error}`, false);
        }
    } catch (error) {
        showMessage(`❌ Error de conexión: ${error.message}`, false);
    }
});

// Actualizar estadísticas
async function updateStats() {
    try {
        const response = await fetch('/api/biometric-data');
        if (response.ok) {
            const data = await response.json();
            const records = data.data || [];
            
            document.getElementById('totalRecords').textContent = records.length;
            
            const relaxed = records.filter(r => r.state === 'relaxed').length;
            const stressed = records.filter(r => r.state === 'stressed').length;
            const meditation = records.filter(r => r.state === 'meditation').length;
            
            document.getElementById('relaxedCount').textContent = relaxed;
            document.getElementById('stressedCount').textContent = stressed;
            document.getElementById('meditationCount').textContent = meditation;
        }
    } catch (error) {
        console.error('Error al actualizar estadísticas:', error);
    }
}

// Cargar estadísticas al iniciar
document.addEventListener('DOMContentLoaded', updateStats);

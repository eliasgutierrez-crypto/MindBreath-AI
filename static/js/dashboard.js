// dashboard.js - Página de dashboard

let allData = [];
let currentPage = 1;
let itemsPerPage = 10;
let filteredData = [];

const tableBody = document.getElementById('tableBody');
const searchInput = document.getElementById('searchInput');
const refreshBtn = document.getElementById('refreshBtn');
const exportBtn = document.getElementById('exportBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const pageInfo = document.getElementById('pageInfo');

// Cargar datos
async function loadData() {
    try {
        const response = await fetch('/api/biometric-data');
        if (response.ok) {
            const result = await response.json();
            allData = result.data || [];
            filteredData = [...allData];
            currentPage = 1;
            renderTable();
            updateAnalytics();
        }
    } catch (error) {
        console.error('Error al cargar datos:', error);
        tableBody.innerHTML = '<tr><td colspan="7" class="text-center">Error al cargar datos</td></tr>';
    }
}

// Renderizar tabla
function renderTable() {
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageData = filteredData.slice(start, end);

    if (pageData.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="7" class="text-center">No hay datos disponibles</td></tr>';
        return;
    }

    tableBody.innerHTML = pageData.map(record => `
        <tr>
            <td>${record.id}</td>
            <td>${new Date(record.timestamp).toLocaleString('es-ES')}</td>
            <td>
                <span style="background: ${getStateColor(record.state)}; color: white; padding: 5px 10px; border-radius: 3px;">
                    ${getStateLabel(record.state)}
                </span>
            </td>
            <td>${record.breathing_rate}</td>
            <td>${record.heart_rate}</td>
            <td>${record.movement}</td>
            <td>${getStressLabel(record.stress_level)}</td>
        </tr>
    `).join('');

    updatePagination();
}

// Obtener color del estado
function getStateColor(state) {
    const colors = {
        'relaxed': '#48bb78',
        'stressed': '#f56565',
        'meditation': '#667eea'
    };
    return colors[state] || '#a0aec0';
}

// Obtener label del estado
function getStateLabel(state) {
    const labels = {
        'relaxed': 'Relajado',
        'stressed': 'Estresado',
        'meditation': 'Meditación'
    };
    return labels[state] || state;
}

// Obtener label del estrés
function getStressLabel(stress) {
    const labels = {
        'low': 'Bajo',
        'medium': 'Medio',
        'high': 'Alto'
    };
    return labels[stress] || stress;
}

// Actualizar paginación
function updatePagination() {
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    pageInfo.textContent = `Página ${currentPage} de ${totalPages}`;
    
    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages;
}

// Actualizar análisis
function updateAnalytics() {
    if (allData.length === 0) {
        document.getElementById('avgHeartRate').textContent = '-';
        document.getElementById('avgBreathingRate').textContent = '-';
        document.getElementById('avgMovement').textContent = '-';
        document.getElementById('totalRecordsAnalytics').textContent = '0';
        return;
    }

    const avgHeartRate = (allData.reduce((sum, r) => sum + r.heart_rate, 0) / allData.length).toFixed(2);
    const avgBreathingRate = (allData.reduce((sum, r) => sum + r.breathing_rate, 0) / allData.length).toFixed(2);
    const avgMovement = (allData.reduce((sum, r) => sum + r.movement, 0) / allData.length).toFixed(2);

    document.getElementById('avgHeartRate').textContent = avgHeartRate + ' bpm';
    document.getElementById('avgBreathingRate').textContent = avgBreathingRate + ' breaths/min';
    document.getElementById('avgMovement').textContent = avgMovement + '%';
    document.getElementById('totalRecordsAnalytics').textContent = allData.length;
}

// Event listeners
searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    filteredData = allData.filter(record => 
        getStateLabel(record.state).toLowerCase().includes(searchTerm) ||
        record.id.toString().includes(searchTerm)
    );
    currentPage = 1;
    renderTable();
});

refreshBtn.addEventListener('click', loadData);

prevBtn.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        renderTable();
        window.scrollTo(0, 0);
    }
});

nextBtn.addEventListener('click', () => {
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        renderTable();
        window.scrollTo(0, 0);
    }
});

exportBtn.addEventListener('click', () => {
    if (allData.length === 0) {
        alert('No hay datos para exportar');
        return;
    }

    let csv = 'ID,Timestamp,Estado,Frecuencia Respiratoria,Frecuencia Cardíaca,Movimiento,Nivel de Estrés\n';
    
    allData.forEach(record => {
        csv += `${record.id},"${new Date(record.timestamp).toLocaleString('es-ES')}","${getStateLabel(record.state)}",${record.breathing_rate},${record.heart_rate},${record.movement},"${getStressLabel(record.stress_level)}"\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `mindbreath_data_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});

// Cargar datos al iniciar
document.addEventListener('DOMContentLoaded', loadData);

// Dashboard JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    initializeDashboard();
    
    // Update data every 30 seconds
    setInterval(updateDashboardData, 30000);
});

function initializeDashboard() {
    // Animate stats on load
    animateStats();
    
    // Initialize real-time clock
    updateClock();
    setInterval(updateClock, 1000);
    
    // Load recent threats
    loadRecentThreats();
    
    // Load training progress
    loadTrainingProgress();
    
    // Initialize system status
    updateSystemStatus();
}

function animateStats() {
    const statValues = document.querySelectorAll('.stat-value');
    
    statValues.forEach(stat => {
        const finalValue = stat.textContent;
        const isNumber = !isNaN(parseInt(finalValue));
        
        if (isNumber) {
            const finalNum = parseInt(finalValue);
            let currentNum = 0;
            const increment = finalNum / 50;
            
            const timer = setInterval(() => {
                currentNum += increment;
                if (currentNum >= finalNum) {
                    currentNum = finalNum;
                    clearInterval(timer);
                }
                stat.textContent = Math.floor(currentNum);
            }, 20);
        }
    });
}

function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('nl-NL', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    
    const clockElement = document.querySelector('.last-login');
    if (clockElement) {
        clockElement.textContent = `Laatst ingelogd: vandaag ${timeString}`;
    }
}

function loadRecentThreats() {
    // Simulate real-time threat data
    const threats = [
        {
            type: 'Phishing Email',
            target: 'marketing@euramax.nl',
            time: formatTimeAgo(new Date(Date.now() - 1000 * 60 * 30)), // 30 min ago
            status: 'Geblokkeerd',
            severity: 'high'
        },
        {
            type: 'Malicious Link',
            target: 'verkoop@euramax.nl',
            time: formatTimeAgo(new Date(Date.now() - 1000 * 60 * 75)), // 75 min ago
            status: 'Geblokkeerd',
            severity: 'medium'
        },
        {
            type: 'Verdachte Bijlage',
            target: 'hr@euramax.nl',
            time: formatTimeAgo(new Date(Date.now() - 1000 * 60 * 120)), // 2 hours ago
            status: 'In Onderzoek',
            severity: 'warning'
        }
    ];
    
    updateThreatList(threats);
}

function updateThreatList(threats) {
    const threatList = document.querySelector('.threat-list');
    if (!threatList) return;
    
    threatList.innerHTML = threats.map(threat => `
        <div class="threat-item ${threat.severity === 'warning' ? 'warning' : 'blocked'}">
            <div class="threat-info">
                <div class="threat-type">${threat.type}</div>
                <div class="threat-target">${threat.target}</div>
                <div class="threat-time">${threat.time}</div>
            </div>
            <div class="threat-status">${threat.status}</div>
        </div>
    `).join('');
}

function loadTrainingProgress() {
    const departments = [
        { name: 'IT Afdeling', progress: 100 },
        { name: 'Marketing', progress: 95 },
        { name: 'Verkoop', progress: 87 },
        { name: 'HR', progress: 92 },
        { name: 'Financiën', progress: 89 },
        { name: 'Operations', progress: 94 }
    ];
    
    updateTrainingProgress(departments);
}

function updateTrainingProgress(departments) {
    const progressContainer = document.querySelector('.training-progress');
    if (!progressContainer) return;
    
    progressContainer.innerHTML = departments.map(dept => `
        <div class="progress-item">
            <div class="department">${dept.name}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${dept.progress}%"></div>
            </div>
            <div class="progress-text">${dept.progress}%</div>
        </div>
    `).join('');
    
    // Animate progress bars
    setTimeout(() => {
        const progressFills = document.querySelectorAll('.progress-fill');
        progressFills.forEach(fill => {
            const width = fill.style.width;
            fill.style.width = '0%';
            setTimeout(() => {
                fill.style.width = width;
            }, 100);
        });
    }, 100);
}

function updateSystemStatus() {
    const systemComponents = [
        { name: 'AI Engine', status: 'Online', uptime: '99.9%' },
        { name: 'Email Scanner', status: 'Online', uptime: '99.8%' },
        { name: 'Database', status: 'Online', uptime: '99.9%' },
        { name: 'Backup System', status: 'Onderhoud', uptime: 'Verwacht eind: 16:00' }
    ];
    
    const statusContainer = document.querySelector('.system-status');
    if (!statusContainer) return;
    
    statusContainer.innerHTML = systemComponents.map(component => `
        <div class="status-item">
            <div class="status-indicator ${component.status === 'Online' ? 'online' : 'warning'}"></div>
            <div class="status-label">${component.name}</div>
            <div class="status-value">${component.status}</div>
        </div>
    `).join('');
}

function updateDashboardData() {
    // Simulate real-time updates
    loadRecentThreats();
    updateSystemStatus();
    
    // Update threat level randomly (simulate changes)
    const threatLevels = ['Laag', 'Gemiddeld', 'Hoog'];
    const colors = ['green', 'orange', 'red'];
    const randomLevel = Math.floor(Math.random() * 3);
    
    const threatLevelElement = document.querySelector('.stat-value.green');
    if (threatLevelElement) {
        threatLevelElement.textContent = threatLevels[randomLevel];
        threatLevelElement.className = `stat-value ${colors[randomLevel]}`;
    }
    
    console.log('Dashboard data updated at', new Date().toLocaleTimeString('nl-NL'));
}

function formatTimeAgo(date) {
    const now = new Date();
    const diffInMinutes = Math.floor((now - date) / (1000 * 60));
    
    if (diffInMinutes < 60) {
        return `${diffInMinutes} min geleden`;
    } else if (diffInMinutes < 1440) { // less than 24 hours
        const hours = Math.floor(diffInMinutes / 60);
        return `${hours} uur geleden`;
    } else {
        const days = Math.floor(diffInMinutes / 1440);
        return `${days} dag${days > 1 ? 'en' : ''} geleden`;
    }
}

// Quick action handlers
document.addEventListener('click', function(e) {
    if (e.target.matches('.action-btn')) {
        e.preventDefault();
        const actionType = e.target.querySelector('.action-text').textContent;
        showNotification(`Navigeer naar ${actionType}...`, 'info');
    }
    
    if (e.target.matches('.view-all')) {
        e.preventDefault();
        showNotification('Alle items laden...', 'info');
    }
});

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#dc3545' : type === 'success' ? '#28a745' : '#007bff'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Close button handler
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (document.body.contains(notification)) {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }
    }, 5000);
}
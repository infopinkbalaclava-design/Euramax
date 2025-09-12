// Support System JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeSupportSystem();
});

function initializeSupportSystem() {
    // Initialize tabs
    initializeTabs();
    
    // Initialize ticket form
    initializeTicketForm();
    
    // Initialize ticket list
    initializeTicketList();
    
    // Initialize knowledge base
    initializeKnowledgeBase();
    
    // Initialize system status
    initializeSystemStatus();
    
    // Auto-save form data
    initializeAutoSave();
}

function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
                
                // Load tab-specific content
                loadTabContent(targetTab);
            }
            
            // Update URL
            const url = new URL(window.location);
            url.searchParams.set('tab', targetTab);
            history.pushState(null, null, url);
        });
    });
    
    // Load initial tab from URL
    const urlParams = new URLSearchParams(window.location.search);
    const initialTab = urlParams.get('tab') || 'new-ticket';
    const initialButton = document.querySelector(`[data-tab="${initialTab}"]`);
    if (initialButton) {
        initialButton.click();
    }
}

function loadTabContent(tabName) {
    switch (tabName) {
        case 'my-tickets':
            loadMyTickets();
            break;
        case 'knowledge-base':
            initializeKBSearch();
            break;
        case 'system-status':
            updateSystemStatus();
            break;
    }
}

function initializeTicketForm() {
    const form = document.getElementById('ticketForm');
    if (!form) return;
    
    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        submitTicket();
    });
    
    // Handle file uploads
    const fileInput = document.getElementById('attachments');
    const fileList = document.getElementById('fileList');
    
    if (fileInput && fileList) {
        fileInput.addEventListener('change', function(e) {
            displaySelectedFiles(e.target.files, fileList);
        });
    }
    
    // Auto-populate user info (simulate logged-in user)
    populateUserInfo();
    
    // Category-specific field updates
    const categorySelect = document.getElementById('category');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            updateFormBasedOnCategory(this.value);
        });
    }
    
    // Priority-based styling
    const prioritySelect = document.getElementById('priority');
    if (prioritySelect) {
        prioritySelect.addEventListener('change', function() {
            updatePriorityIndicator(this.value);
        });
    }
}

function populateUserInfo() {
    // Simulate getting user info from session/JWT
    const userData = {
        name: 'Jan Janssen',
        email: 'j.janssen@euramax.nl',
        department: 'it'
    };
    
    const nameField = document.getElementById('employee-name');
    const emailField = document.getElementById('employee-email');
    const departmentField = document.getElementById('department');
    
    if (nameField && !nameField.value) nameField.value = userData.name;
    if (emailField && !emailField.value) emailField.value = userData.email;
    if (departmentField && !departmentField.value) departmentField.value = userData.department;
}

function updateFormBasedOnCategory(category) {
    const descriptionField = document.getElementById('description');
    if (!descriptionField) return;
    
    const categoryPrompts = {
        'phishing-detection': 'Beschrijf de verdachte email of bedreiging die niet werd gedetecteerd. Voeg indien mogelijk de email headers toe.',
        'false-positive': 'Beschrijf welke legitieme email of link ten onrechte werd geblokkeerd. Vermeld de afzender en tijdstip.',
        'training': 'Beschrijf welke training je nodig hebt of welk probleem je ondervindt met de huidige trainingsmaterialen.',
        'login-access': 'Beschrijf het inlogprobleem. Vermeld eventuele foutmeldingen en of je VPN-verbinding actief is.',
        'dashboard': 'Beschrijf het probleem met het dashboard. Vermeld je browser en apparaat type.',
        'performance': 'Beschrijf de performance problemen. Hoe lang duurt het laden en wanneer treedt dit op?'
    };
    
    if (categoryPrompts[category]) {
        descriptionField.placeholder = categoryPrompts[category];
    }
}

function updatePriorityIndicator(priority) {
    const form = document.querySelector('.support-form');
    if (!form) return;
    
    // Remove existing priority classes
    form.classList.remove('priority-critical', 'priority-high', 'priority-medium', 'priority-low');
    
    // Add new priority class
    if (priority) {
        form.classList.add(`priority-${priority}`);
        
        // Show escalation notice for critical issues
        if (priority === 'critical') {
            showCriticalPriorityNotice();
        }
    }
}

function showCriticalPriorityNotice() {
    let notice = document.querySelector('.critical-notice');
    if (notice) return; // Already shown
    
    notice = document.createElement('div');
    notice.className = 'critical-notice';
    notice.innerHTML = `
        <div class="alert critical-alert">
            <strong>⚠️ Kritieke Prioriteit Geselecteerd</strong><br>
            Voor directe beveiligingsincidenten bel ook: <strong>+31 6 1234 5678</strong> (24/7)<br>
            Dit ticket wordt automatisch doorgestuurd naar het security team.
        </div>
    `;
    
    notice.style.cssText = `
        margin: 1rem 0;
    `;
    
    const priorityField = document.getElementById('priority').closest('.form-group');
    priorityField.parentNode.insertBefore(notice, priorityField.nextSibling);
}

function displaySelectedFiles(files, container) {
    container.innerHTML = '';
    
    Array.from(files).forEach(file => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <span class="file-name">📎 ${file.name}</span>
            <span class="file-size">(${formatFileSize(file.size)})</span>
            <button type="button" class="remove-file" data-filename="${file.name}">×</button>
        `;
        
        fileItem.style.cssText = `
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem;
            background: #f8f9fa;
            border-radius: 4px;
            margin-bottom: 0.25rem;
        `;
        
        container.appendChild(fileItem);
    });
    
    // Remove file functionality
    container.addEventListener('click', function(e) {
        if (e.target.matches('.remove-file')) {
            e.target.closest('.file-item').remove();
            // In a real implementation, you'd remove the file from the input
        }
    });
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function submitTicket() {
    const form = document.getElementById('ticketForm');
    const formData = new FormData(form);
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Ticket wordt ingediend...';
    submitBtn.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        const ticketId = generateTicketId();
        showTicketSubmissionSuccess(ticketId);
        
        // Reset form
        form.reset();
        populateUserInfo();
        
        // Reset button
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        
        // Clear auto-save
        clearAutoSavedData();
        
        // Switch to my tickets tab
        setTimeout(() => {
            const myTicketsTab = document.querySelector('[data-tab="my-tickets"]');
            if (myTicketsTab) {
                myTicketsTab.click();
            }
        }, 2000);
        
    }, 2000);
}

function generateTicketId() {
    const prefix = 'SEC';
    const year = new Date().getFullYear();
    const random = Math.floor(Math.random() * 9999).toString().padStart(4, '0');
    return `${prefix}-${year}-${random}`;
}

function showTicketSubmissionSuccess(ticketId) {
    const modal = document.createElement('div');
    modal.className = 'success-modal';
    modal.innerHTML = `
        <div class="modal-overlay">
            <div class="modal-content success">
                <div class="success-icon">✅</div>
                <h3>Ticket Succesvol Ingediend!</h3>
                <p>Je support ticket is aangemaakt met ID: <strong>${ticketId}</strong></p>
                <p>Je ontvangt een bevestiging per email en ons team zal zo snel mogelijk reageren.</p>
                <div class="expected-response">
                    <strong>Verwachte responstijd:</strong> binnen 2 uur
                </div>
                <button class="btn btn-primary close-modal">Oké</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Style modal
    const overlay = modal.querySelector('.modal-overlay');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
    `;
    
    const content = modal.querySelector('.modal-content');
    content.style.cssText = `
        background: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        max-width: 400px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    `;
    
    // Close modal
    modal.querySelector('.close-modal').addEventListener('click', () => {
        document.body.removeChild(modal);
    });
}

function initializeTicketList() {
    // Ticket action handlers
    document.addEventListener('click', function(e) {
        if (e.target.matches('.btn-view')) {
            e.preventDefault();
            const ticketItem = e.target.closest('.ticket-item');
            const ticketId = ticketItem.querySelector('.ticket-id').textContent;
            viewTicketDetails(ticketId);
        }
        
        if (e.target.matches('.btn-reply')) {
            e.preventDefault();
            const ticketItem = e.target.closest('.ticket-item');
            const ticketId = ticketItem.querySelector('.ticket-id').textContent;
            openReplyModal(ticketId);
        }
        
        if (e.target.matches('.btn-rate')) {
            e.preventDefault();
            const ticketItem = e.target.closest('.ticket-item');
            const ticketId = ticketItem.querySelector('.ticket-id').textContent;
            openRatingModal(ticketId);
        }
    });
    
    // Filter functionality
    const filterSelect = document.querySelector('.tickets-filters .filter-select');
    if (filterSelect) {
        filterSelect.addEventListener('change', function() {
            filterTickets(this.value);
        });
    }
}

function loadMyTickets() {
    // Simulate loading user's tickets
    const ticketsContainer = document.querySelector('.tickets-list');
    if (!ticketsContainer) return;
    
    // Add loading state
    ticketsContainer.innerHTML = '<div class="loading">Tickets laden...</div>';
    
    setTimeout(() => {
        // Tickets are already in HTML, but we could load them dynamically
        console.log('My tickets loaded');
    }, 500);
}

function filterTickets(status) {
    const tickets = document.querySelectorAll('.ticket-item');
    
    tickets.forEach(ticket => {
        const ticketStatus = ticket.classList[1]; // e.g., 'open', 'in-progress', 'resolved'
        
        if (status === 'all' || ticket.classList.contains(status)) {
            ticket.style.display = 'block';
        } else {
            ticket.style.display = 'none';
        }
    });
}

function initializeKnowledgeBase() {
    // KB article click handlers
    document.addEventListener('click', function(e) {
        if (e.target.matches('.kb-article') || e.target.closest('.kb-article')) {
            e.preventDefault();
            const article = e.target.closest('.kb-article') || e.target;
            const title = article.querySelector('h4').textContent;
            openKBArticle(title);
        }
    });
}

function initializeKBSearch() {
    const searchInput = document.querySelector('.kb-search .search-input');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', debounce(function(e) {
        const query = e.target.value.toLowerCase().trim();
        searchKnowledgeBase(query);
    }, 300));
}

function searchKnowledgeBase(query) {
    const articles = document.querySelectorAll('.kb-article');
    let visibleCount = 0;
    
    articles.forEach(article => {
        const title = article.querySelector('h4').textContent.toLowerCase();
        const description = article.querySelector('p').textContent.toLowerCase();
        const matches = !query || title.includes(query) || description.includes(query);
        
        if (matches) {
            article.style.display = 'block';
            visibleCount++;
            
            // Highlight search terms
            if (query) {
                highlightSearchTerms(article, query);
            }
        } else {
            article.style.display = 'none';
        }
    });
    
    updateKBSearchResults(query, visibleCount);
}

function highlightSearchTerms(element, query) {
    // Simple highlighting - in production you'd want more sophisticated highlighting
    const titleElement = element.querySelector('h4');
    const originalTitle = titleElement.getAttribute('data-original') || titleElement.textContent;
    
    if (!titleElement.getAttribute('data-original')) {
        titleElement.setAttribute('data-original', originalTitle);
    }
    
    if (query) {
        const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
        const highlightedTitle = originalTitle.replace(regex, '<mark style="background: #ffeb3b;">$1</mark>');
        titleElement.innerHTML = highlightedTitle;
    } else {
        titleElement.textContent = originalTitle;
    }
}

function updateKBSearchResults(query, count) {
    let resultDisplay = document.querySelector('.kb-search-results');
    
    if (query) {
        if (!resultDisplay) {
            resultDisplay = document.createElement('div');
            resultDisplay.className = 'kb-search-results';
            resultDisplay.style.cssText = `
                text-align: center;
                margin: 1rem 0;
                padding: 0.75rem;
                background: #e8f5e8;
                border-radius: 8px;
                color: #2e7d32;
            `;
            
            const kbCategories = document.querySelector('.kb-categories');
            kbCategories.parentNode.insertBefore(resultDisplay, kbCategories);
        }
        
        resultDisplay.textContent = `${count} artikel${count !== 1 ? 'en' : ''} gevonden voor "${query}"`;
    } else if (resultDisplay) {
        resultDisplay.remove();
    }
}

function openKBArticle(title) {
    // Simulate opening a knowledge base article
    showNotification(`Knowledge base artikel wordt geopend: ${title}`, 'info');
}

function initializeSystemStatus() {
    // Real-time status updates
    setInterval(updateSystemStatus, 60000); // Update every minute
}

function updateSystemStatus() {
    // Simulate real-time status updates
    const components = document.querySelectorAll('.component');
    
    components.forEach(component => {
        // Randomly update status (simulate real changes)
        if (Math.random() < 0.05) { // 5% chance of status change
            const statusElement = component.querySelector('.component-status');
            const currentStatus = statusElement.textContent;
            
            if (currentStatus === 'Operationeel' && Math.random() < 0.3) {
                statusElement.textContent = 'Onderzoek';
                component.classList.remove('operational');
                component.classList.add('investigating');
            }
        }
    });
}

function initializeAutoSave() {
    const form = document.getElementById('ticketForm');
    if (!form) return;
    
    // Auto-save form data every 30 seconds
    setInterval(() => {
        saveFormData();
    }, 30000);
    
    // Save on input changes
    form.addEventListener('input', debounce(saveFormData, 5000));
    
    // Load saved data on page load
    loadSavedFormData();
}

function saveFormData() {
    const form = document.getElementById('ticketForm');
    if (!form) return;
    
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    localStorage.setItem('support_ticket_draft', JSON.stringify(data));
    console.log('Form data auto-saved');
}

function loadSavedFormData() {
    const savedData = localStorage.getItem('support_ticket_draft');
    if (!savedData) return;
    
    try {
        const data = JSON.parse(savedData);
        const form = document.getElementById('ticketForm');
        
        Object.entries(data).forEach(([key, value]) => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field && !field.value) { // Don't overwrite manually entered data
                field.value = value;
            }
        });
        
        showNotification('Conceptgegevens hersteld', 'info');
    } catch (e) {
        console.error('Error loading saved form data:', e);
    }
}

function clearAutoSavedData() {
    localStorage.removeItem('support_ticket_draft');
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
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
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    });
    
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
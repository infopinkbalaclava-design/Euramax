// Team Directory JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeTeamDirectory();
});

function initializeTeamDirectory() {
    // Initialize filters
    initializeFilters();
    
    // Initialize contact functionality
    initializeContactFeatures();
    
    // Initialize status updates
    initializeStatusUpdates();
    
    // Initialize search functionality
    initializeTeamSearch();
    
    // Load team calendar
    loadTeamCalendar();
}

function initializeFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const teamMembers = document.querySelectorAll('.team-member');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Get filter value
            const filter = this.getAttribute('data-filter');
            
            // Filter team members
            filterTeamMembers(filter, teamMembers);
            
            // Update URL
            const url = new URL(window.location);
            if (filter === 'all') {
                url.searchParams.delete('filter');
            } else {
                url.searchParams.set('filter', filter);
            }
            history.pushState(null, null, url);
        });
    });
    
    // Apply initial filter from URL
    const urlParams = new URLSearchParams(window.location.search);
    const initialFilter = urlParams.get('filter');
    if (initialFilter) {
        const filterButton = document.querySelector(`[data-filter="${initialFilter}"]`);
        if (filterButton) {
            filterButton.click();
        }
    }
}

function filterTeamMembers(filter, teamMembers) {
    teamMembers.forEach(member => {
        const category = member.getAttribute('data-category');
        
        if (filter === 'all' || category === filter) {
            member.style.display = 'block';
            member.style.opacity = '0';
            member.style.transform = 'translateY(20px)';
            
            // Animate in with stagger
            setTimeout(() => {
                member.style.transition = 'all 0.3s ease';
                member.style.opacity = '1';
                member.style.transform = 'translateY(0)';
            }, Math.random() * 200);
        } else {
            member.style.transition = 'all 0.3s ease';
            member.style.opacity = '0';
            member.style.transform = 'translateY(-20px)';
            
            setTimeout(() => {
                member.style.display = 'none';
            }, 300);
        }
    });
    
    // Update count
    updateMemberCount(filter);
}

function updateMemberCount(filter) {
    const totalMembers = document.querySelectorAll('.team-member').length;
    const visibleMembers = document.querySelectorAll(
        filter === 'all' ? '.team-member' : `[data-category="${filter}"]`
    ).length;
    
    // Create or update count display
    let countDisplay = document.querySelector('.member-count');
    if (!countDisplay) {
        countDisplay = document.createElement('div');
        countDisplay.className = 'member-count';
        countDisplay.style.cssText = `
            text-align: center;
            margin: 1rem 0;
            font-weight: 500;
            color: #6c757d;
        `;
        
        const teamGrid = document.querySelector('.team-grid');
        teamGrid.parentNode.insertBefore(countDisplay, teamGrid);
    }
    
    const filterName = filter === 'all' ? 'alle team leden' : 
                      filter === 'development' ? 'development team leden' :
                      filter === 'security' ? 'security team leden' :
                      filter === 'it-support' ? 'IT support team leden' :
                      filter === 'management' ? 'management team leden' : 'team leden';
    
    countDisplay.textContent = `${visibleMembers} van ${totalMembers} ${filterName}`;
}

function initializeContactFeatures() {
    // Contact button handlers
    document.addEventListener('click', function(e) {
        if (e.target.matches('.btn-contact')) {
            e.preventDefault();
            const memberCard = e.target.closest('.team-member');
            const email = memberCard.querySelector('.contact-info span').textContent.replace('📧 ', '');
            openEmailClient(email);
        }
        
        if (e.target.matches('.btn-teams')) {
            e.preventDefault();
            const memberCard = e.target.closest('.team-member');
            const name = memberCard.querySelector('h3').textContent;
            openTeamsChat(name);
        }
    });
}

function openEmailClient(email) {
    const subject = encodeURIComponent('Vraag over Euramax Beveiligingssysteem');
    const body = encodeURIComponent('Hallo,\n\nIk heb een vraag over het Euramax beveiligingssysteem.\n\nMet vriendelijke groet,');
    
    const mailtoLink = `mailto:${email}?subject=${subject}&body=${body}`;
    window.location.href = mailtoLink;
    
    showNotification(`Email client geopend voor ${email}`, 'success');
}

function openTeamsChat(name) {
    // Simulate opening Teams chat
    showNotification(`Teams chat geopend met ${name}`, 'info');
    
    // In a real implementation, this would integrate with Microsoft Teams
    console.log(`Opening Teams chat with ${name}`);
}

function initializeStatusUpdates() {
    // Simulate real-time status updates
    setInterval(updateMemberStatuses, 30000); // Update every 30 seconds
    
    // Add status hover effects
    document.querySelectorAll('.status-indicator').forEach(indicator => {
        indicator.addEventListener('mouseenter', function() {
            const status = this.classList.contains('online') ? 'Online' :
                          this.classList.contains('away') ? 'Afwezig' : 'Offline';
            
            showStatusTooltip(this, status);
        });
        
        indicator.addEventListener('mouseleave', function() {
            hideStatusTooltip();
        });
    });
}

function updateMemberStatuses() {
    const statusIndicators = document.querySelectorAll('.status-indicator');
    
    statusIndicators.forEach(indicator => {
        // Randomly update status (simulate real-time changes)
        if (Math.random() < 0.1) { // 10% chance of status change
            const statuses = ['online', 'away', 'offline'];
            const currentStatus = statuses.find(status => indicator.classList.contains(status));
            const newStatus = statuses[Math.floor(Math.random() * statuses.length)];
            
            if (currentStatus !== newStatus) {
                indicator.classList.remove(currentStatus);
                indicator.classList.add(newStatus);
                
                // Show notification for status change
                const memberName = indicator.closest('.team-member').querySelector('h3').textContent;
                const statusText = newStatus === 'online' ? 'Online' :
                                 newStatus === 'away' ? 'Afwezig' : 'Offline';
                
                console.log(`${memberName} status changed to ${statusText}`);
            }
        }
    });
}

function showStatusTooltip(element, status) {
    hideStatusTooltip(); // Remove existing tooltip
    
    const tooltip = document.createElement('div');
    tooltip.className = 'status-tooltip';
    tooltip.textContent = status;
    tooltip.style.cssText = `
        position: absolute;
        background: #2c3e50;
        color: white;
        padding: 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        z-index: 1000;
        pointer-events: none;
        white-space: nowrap;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
}

function hideStatusTooltip() {
    const tooltip = document.querySelector('.status-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

function initializeTeamSearch() {
    // Add search functionality
    const searchContainer = document.createElement('div');
    searchContainer.className = 'team-search';
    searchContainer.innerHTML = `
        <input type="text" 
               placeholder="Zoek team leden op naam, rol, of afdeling..." 
               class="team-search-input"
               style="width: 100%; max-width: 400px; padding: 0.75rem; border: 2px solid #e9ecef; border-radius: 25px; font-size: 1rem;">
    `;
    
    searchContainer.style.cssText = `
        text-align: center;
        margin-bottom: 2rem;
    `;
    
    const teamFilters = document.querySelector('.team-filters .container');
    teamFilters.appendChild(searchContainer);
    
    const searchInput = searchContainer.querySelector('.team-search-input');
    searchInput.addEventListener('input', debounce(function(e) {
        const query = e.target.value.toLowerCase().trim();
        searchTeamMembers(query);
    }, 300));
}

function searchTeamMembers(query) {
    const teamMembers = document.querySelectorAll('.team-member');
    let visibleCount = 0;
    
    teamMembers.forEach(member => {
        const name = member.querySelector('h3').textContent.toLowerCase();
        const role = member.querySelector('.role').textContent.toLowerCase();
        const department = member.querySelector('.department').textContent.toLowerCase();
        const skills = Array.from(member.querySelectorAll('.skill'))
                          .map(skill => skill.textContent.toLowerCase())
                          .join(' ');
        
        const searchText = `${name} ${role} ${department} ${skills}`;
        const matches = !query || searchText.includes(query);
        
        if (matches) {
            member.style.display = 'block';
            member.style.opacity = '1';
            member.style.transform = 'translateY(0)';
            visibleCount++;
        } else {
            member.style.display = 'none';
            member.style.opacity = '0';
            member.style.transform = 'translateY(-20px)';
        }
    });
    
    // Update search results count
    updateSearchResults(query, visibleCount);
}

function updateSearchResults(query, count) {
    let resultDisplay = document.querySelector('.search-results');
    
    if (query) {
        if (!resultDisplay) {
            resultDisplay = document.createElement('div');
            resultDisplay.className = 'search-results';
            resultDisplay.style.cssText = `
                text-align: center;
                margin: 1rem 0;
                padding: 0.75rem;
                background: #e3f2fd;
                border-radius: 8px;
                font-weight: 500;
                color: #1976d2;
            `;
            
            const teamGrid = document.querySelector('.team-grid');
            teamGrid.parentNode.insertBefore(resultDisplay, teamGrid);
        }
        
        resultDisplay.textContent = `${count} team lid${count !== 1 ? 'en' : ''} gevonden voor "${query}"`;
    } else if (resultDisplay) {
        resultDisplay.remove();
    }
}

function loadTeamCalendar() {
    // Simulate loading calendar events
    const events = [
        {
            date: '18 maart',
            title: 'Security Review Meeting',
            description: 'Maandelijkse security review met management',
            attendees: ['Emma', 'Robert', 'Anna']
        },
        {
            date: '22 maart',
            title: 'System Maintenance',
            description: 'Geplande server updates (2:00-4:00 AM)',
            attendees: ['Tom', 'Jan']
        },
        {
            date: '25 maart',
            title: 'Sprint Planning',
            description: 'Development team sprint planning sessie',
            attendees: ['Development Team']
        }
    ];
    
    // Events are already in HTML, but we could make them interactive
    const eventItems = document.querySelectorAll('.event-item');
    eventItems.forEach((item, index) => {
        if (events[index]) {
            item.addEventListener('click', function() {
                showEventDetails(events[index]);
            });
            
            item.style.cursor = 'pointer';
            item.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(10px)';
                this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.1)';
            });
            
            item.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0)';
                this.style.boxShadow = 'none';
            });
        }
    });
}

function showEventDetails(event) {
    const modal = document.createElement('div');
    modal.className = 'event-modal';
    modal.innerHTML = `
        <div class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${event.title}</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    <p><strong>Datum:</strong> ${event.date}</p>
                    <p><strong>Beschrijving:</strong> ${event.description}</p>
                    <p><strong>Deelnemers:</strong> ${event.attendees.join(', ')}</p>
                </div>
                <div class="modal-actions">
                    <button class="btn btn-primary">Voeg toe aan Kalender</button>
                    <button class="btn btn-secondary modal-close">Sluiten</button>
                </div>
            </div>
        </div>
    `;
    
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 2000;
    `;
    
    document.body.appendChild(modal);
    
    // Modal styles
    const overlay = modal.querySelector('.modal-overlay');
    overlay.style.cssText = `
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    `;
    
    const content = modal.querySelector('.modal-content');
    content.style.cssText = `
        background: white;
        border-radius: 12px;
        max-width: 500px;
        width: 100%;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    `;
    
    // Close modal functionality
    const closeButtons = modal.querySelectorAll('.modal-close');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            document.body.removeChild(modal);
        });
    });
    
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            document.body.removeChild(modal);
        }
    });
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
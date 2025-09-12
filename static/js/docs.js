// Documentation JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeDocumentation();
});

function initializeDocumentation() {
    // Initialize search functionality
    initializeSearch();
    
    // Initialize navigation
    initializeNavigation();
    
    // Initialize code block features
    initializeCodeBlocks();
    
    // Initialize section anchors
    initializeSectionAnchors();
    
    // Initialize print functionality
    initializePrintFeatures();
}

function initializeSearch() {
    const searchInput = document.getElementById('docs-search');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', debounce(function(e) {
        const query = e.target.value.toLowerCase().trim();
        searchDocumentation(query);
    }, 300));
    
    // Add search icon functionality
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const query = e.target.value.toLowerCase().trim();
            if (query) {
                searchDocumentation(query);
                showSearchResults(query);
            }
        }
    });
}

function searchDocumentation(query) {
    if (!query) {
        clearSearchHighlights();
        return;
    }
    
    // Clear previous highlights
    clearSearchHighlights();
    
    // Search in navigation
    const navLinks = document.querySelectorAll('.docs-nav a');
    navLinks.forEach(link => {
        const text = link.textContent.toLowerCase();
        if (text.includes(query)) {
            link.classList.add('search-match');
        }
    });
    
    // Search in content
    const sections = document.querySelectorAll('.docs-section');
    let matchCount = 0;
    
    sections.forEach(section => {
        const content = section.textContent.toLowerCase();
        if (content.includes(query)) {
            section.classList.add('search-match');
            highlightTextInElement(section, query);
            matchCount++;
        }
    });
    
    // Show search status
    showSearchStatus(query, matchCount);
}

function highlightTextInElement(element, query) {
    const walker = document.createTreeWalker(
        element,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    const textNodes = [];
    let node;
    
    while (node = walker.nextNode()) {
        if (node.parentElement.tagName !== 'SCRIPT' && 
            node.parentElement.tagName !== 'STYLE') {
            textNodes.push(node);
        }
    }
    
    textNodes.forEach(textNode => {
        const content = textNode.textContent;
        const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
        
        if (regex.test(content)) {
            const highlightedContent = content.replace(regex, '<mark class="search-highlight">$1</mark>');
            const wrapper = document.createElement('span');
            wrapper.innerHTML = highlightedContent;
            
            textNode.parentNode.replaceChild(wrapper, textNode);
        }
    });
}

function clearSearchHighlights() {
    // Remove search match classes
    document.querySelectorAll('.search-match').forEach(el => {
        el.classList.remove('search-match');
    });
    
    // Remove highlight marks
    document.querySelectorAll('.search-highlight').forEach(mark => {
        const parent = mark.parentNode;
        parent.replaceChild(document.createTextNode(mark.textContent), mark);
        parent.normalize();
    });
    
    // Clear search status
    const statusElement = document.querySelector('.search-status');
    if (statusElement) {
        statusElement.remove();
    }
}

function showSearchStatus(query, count) {
    // Remove existing status
    const existingStatus = document.querySelector('.search-status');
    if (existingStatus) {
        existingStatus.remove();
    }
    
    // Create new status
    const status = document.createElement('div');
    status.className = 'search-status';
    status.innerHTML = `
        <div class="search-status-content">
            <strong>${count}</strong> resultaten gevonden voor "${query}"
            <button class="clear-search" onclick="clearSearch()">×</button>
        </div>
    `;
    
    status.style.cssText = `
        background: #e3f2fd;
        border: 1px solid #2196f3;
        border-radius: 6px;
        padding: 0.75rem;
        margin: 1rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    `;
    
    const docsContent = document.querySelector('.docs-content');
    docsContent.insertBefore(status, docsContent.firstChild);
}

function clearSearch() {
    const searchInput = document.getElementById('docs-search');
    if (searchInput) {
        searchInput.value = '';
    }
    clearSearchHighlights();
}

function initializeNavigation() {
    const navLinks = document.querySelectorAll('.docs-nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Scroll to section
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update URL
                history.pushState(null, null, `#${targetId}`);
            }
        });
    });
    
    // Handle back/forward navigation
    window.addEventListener('popstate', function() {
        const hash = window.location.hash.substring(1);
        if (hash) {
            const targetSection = document.getElementById(hash);
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update active nav link
                navLinks.forEach(l => l.classList.remove('active'));
                const activeLink = document.querySelector(`.docs-nav a[href="#${hash}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        }
    });
    
    // Set initial active link based on URL hash
    const initialHash = window.location.hash.substring(1);
    if (initialHash) {
        const activeLink = document.querySelector(`.docs-nav a[href="#${initialHash}"]`);
        if (activeLink) {
            navLinks.forEach(l => l.classList.remove('active'));
            activeLink.classList.add('active');
        }
    }
}

function initializeCodeBlocks() {
    const codeBlocks = document.querySelectorAll('.code-block');
    
    codeBlocks.forEach(block => {
        // Add copy button
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-code-btn';
        copyBtn.innerHTML = '📋 Kopieer';
        copyBtn.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        // Make code block relative positioned
        block.style.position = 'relative';
        block.appendChild(copyBtn);
        
        // Show/hide copy button on hover
        block.addEventListener('mouseenter', () => {
            copyBtn.style.opacity = '1';
        });
        
        block.addEventListener('mouseleave', () => {
            copyBtn.style.opacity = '0';
        });
        
        // Copy functionality
        copyBtn.addEventListener('click', async () => {
            const code = block.querySelector('pre code')?.textContent || block.querySelector('pre')?.textContent || '';
            
            try {
                await navigator.clipboard.writeText(code);
                copyBtn.innerHTML = '✅ Gekopieerd!';
                setTimeout(() => {
                    copyBtn.innerHTML = '📋 Kopieer';
                }, 2000);
            } catch (err) {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = code;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                copyBtn.innerHTML = '✅ Gekopieerd!';
                setTimeout(() => {
                    copyBtn.innerHTML = '📋 Kopieer';
                }, 2000);
            }
        });
    });
}

function initializeSectionAnchors() {
    // Add anchor links to headings
    const headings = document.querySelectorAll('.docs-section h2, .docs-section h3, .docs-section h4');
    
    headings.forEach(heading => {
        if (!heading.id) {
            // Generate ID from heading text
            const id = heading.textContent
                .toLowerCase()
                .replace(/[^a-z0-9\s-]/g, '')
                .replace(/\s+/g, '-')
                .trim();
            heading.id = id;
        }
        
        // Add anchor link
        const anchor = document.createElement('a');
        anchor.className = 'section-anchor';
        anchor.href = `#${heading.id}`;
        anchor.innerHTML = '🔗';
        anchor.style.cssText = `
            margin-left: 0.5rem;
            opacity: 0;
            transition: opacity 0.3s ease;
            text-decoration: none;
            font-size: 0.8em;
        `;
        
        heading.appendChild(anchor);
        
        // Show anchor on hover
        heading.addEventListener('mouseenter', () => {
            anchor.style.opacity = '0.6';
        });
        
        heading.addEventListener('mouseleave', () => {
            anchor.style.opacity = '0';
        });
        
        // Click handler
        anchor.addEventListener('click', (e) => {
            e.preventDefault();
            const url = new URL(window.location);
            url.hash = heading.id;
            history.pushState(null, null, url);
            
            heading.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    });
}

function initializePrintFeatures() {
    // Add print button
    const printBtn = document.createElement('button');
    printBtn.innerHTML = '🖨️ Print Documentatie';
    printBtn.className = 'print-docs-btn';
    printBtn.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: #007bff;
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 25px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,123,255,0.3);
        font-weight: 500;
        transition: all 0.3s ease;
        z-index: 100;
    `;
    
    printBtn.addEventListener('mouseenter', () => {
        printBtn.style.transform = 'translateY(-2px)';
        printBtn.style.boxShadow = '0 6px 20px rgba(0,123,255,0.4)';
    });
    
    printBtn.addEventListener('mouseleave', () => {
        printBtn.style.transform = 'translateY(0)';
        printBtn.style.boxShadow = '0 4px 12px rgba(0,123,255,0.3)';
    });
    
    printBtn.addEventListener('click', () => {
        window.print();
    });
    
    document.body.appendChild(printBtn);
    
    // Hide print button on mobile
    if (window.innerWidth < 768) {
        printBtn.style.display = 'none';
    }
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

// Export for global access
window.docsHelpers = {
    clearSearch,
    searchDocumentation
};
// Main JavaScript for Dhan Copy Trader

// Initialize Socket.IO connection
const socket = io();

// Connection status management
const statusIndicator = document.getElementById('status-indicator');
const statusText = document.getElementById('status-text');

// Socket event handlers
socket.on('connect', function() {
    updateConnectionStatus('connected', 'Connected');
    console.log('Connected to server');
});

socket.on('disconnect', function() {
    updateConnectionStatus('disconnected', 'Disconnected');
    console.log('Disconnected from server');
});

socket.on('status', function(data) {
    console.log('Status update:', data);
    showNotification(data.message, 'info');
});

socket.on('margin_update', function(data) {
    console.log('Margin update:', data);
    if (typeof updateMarginsTable === 'function') {
        updateMarginsTable(data);
    }
});

socket.on('status_update', function(data) {
    console.log('Trading status update:', data);
    updateTradingStatus(data);
});

socket.on('order_update', function(data) {
    console.log('Order update:', data);
    if (typeof addTradingFeedItem === 'function') {
        addTradingFeedItem('Order Update', JSON.stringify(data), 'info');
    }
});

// Connection status helper
function updateConnectionStatus(status, text) {
    if (!statusIndicator || !statusText) return;
    
    statusIndicator.className = 'bi bi-circle-fill';
    statusText.textContent = text;
    
    switch (status) {
        case 'connected':
            statusIndicator.classList.add('text-success');
            break;
        case 'disconnected':
            statusIndicator.classList.add('text-danger');
            break;
        case 'connecting':
            statusIndicator.classList.add('text-warning');
            break;
    }
}

// Trading status update helper
function updateTradingStatus(data) {
    // Update master status
    const masterStatus = document.getElementById('master-status');
    if (masterStatus) {
        if (data.master_connected) {
            masterStatus.innerHTML = '<i class="bi bi-circle-fill text-success"></i> Connected';
        } else {
            masterStatus.innerHTML = '<i class="bi bi-circle-fill text-danger"></i> Disconnected';
        }
    }
    
    // Update child count
    const childCount = document.getElementById('child-count');
    if (childCount) {
        childCount.textContent = data.children_count || 0;
    }
    
    // Update trading status
    const tradingStatus = document.getElementById('trading-status');
    if (tradingStatus) {
        if (data.active) {
            tradingStatus.innerHTML = '<i class="bi bi-play-circle text-success"></i> Active';
        } else {
            tradingStatus.innerHTML = '<i class="bi bi-pause-circle text-warning"></i> Inactive';
        }
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const alertTypes = {
        'info': 'alert-info',
        'success': 'alert-success',
        'warning': 'alert-warning',
        'error': 'alert-danger'
    };
    
    const alertClass = alertTypes[type] || 'alert-info';
    
    const notification = document.createElement('div');
    notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// API helper functions
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        showNotification(`API Error: ${error.message}`, 'error');
        throw error;
    }
}

// Format currency helper
function formatCurrency(amount, currency = '₹') {
    if (typeof amount !== 'number') {
        amount = parseFloat(amount) || 0;
    }
    return `${currency}${amount.toLocaleString('en-IN')}`;
}

// Format percentage helper
function formatPercentage(value, decimals = 1) {
    if (typeof value !== 'number') {
        value = parseFloat(value) || 0;
    }
    return `${value.toFixed(decimals)}%`;
}

// Loading state management
function setLoadingState(element, isLoading = true) {
    if (!element) return;
    
    if (isLoading) {
        element.classList.add('loading');
        element.style.position = 'relative';
    } else {
        element.classList.remove('loading');
    }
}

// Form validation helper
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Auto-refresh functionality
let autoRefreshInterval = null;

function startAutoRefresh(callback, interval = 30000) {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    
    autoRefreshInterval = setInterval(callback, interval);
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Set initial connection status
    updateConnectionStatus('connecting', 'Connecting...');
    
    console.log('Dhan Copy Trader initialized');
});

// Handle form submissions with AJAX
function handleFormSubmit(formElement, submitUrl, onSuccess) {
    formElement.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!validateForm(formElement)) {
            showNotification('Please fill in all required fields', 'warning');
            return;
        }
        
        const formData = new FormData(formElement);
        const data = Object.fromEntries(formData.entries());
        
        setLoadingState(formElement);
        
        try {
            const response = await apiRequest(submitUrl, 'POST', data);
            
            if (response.success) {
                showNotification('Settings saved successfully', 'success');
                if (onSuccess) {
                    onSuccess(response);
                }
            } else {
                showNotification(response.error || 'An error occurred', 'error');
            }
        } catch (error) {
            console.error('Form submission error:', error);
        } finally {
            setLoadingState(formElement, false);
        }
    });
}

// Utility functions for common tasks
const Utils = {
    // Copy text to clipboard
    copyToClipboard: async function(text) {
        try {
            await navigator.clipboard.writeText(text);
            showNotification('Copied to clipboard', 'success');
            return true;
        } catch (err) {
            console.error('Failed to copy: ', err);
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                showNotification('Copied to clipboard', 'success');
                return true;
            } catch (fallbackErr) {
                showNotification('Failed to copy to clipboard', 'error');
                return false;
            } finally {
                document.body.removeChild(textArea);
            }
        }
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Time formatting
    formatTime: function(timestamp) {
        return new Date(timestamp).toLocaleString('en-IN');
    },
    
    // Confirmation dialog
    confirm: function(message, callback) {
        if (window.confirm(message)) {
            callback();
        }
    }
};

// Export utilities for global access
window.Utils = Utils;
window.showNotification = showNotification;
window.apiRequest = apiRequest;
window.formatCurrency = formatCurrency;
window.formatPercentage = formatPercentage;
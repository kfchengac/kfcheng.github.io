// COLLIDE AI - Admin Dashboard JavaScript

// Show section
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.admin-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionName + '-section').classList.add('active');
    
    // Update nav
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Load data for conversations section
    if (sectionName === 'conversations') {
        loadConversations();
    }
}

// API Settings Form
document.getElementById('api-settings-form')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const settings = {
        openai_api_key: formData.get('openai_api_key'),
        model: formData.get('model'),
        use_api: formData.get('use_api') === 'true'
    };
    
    try {
        const response = await fetch('/admin/api/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        });
        
        if (response.ok) {
            showNotification('API settings saved successfully!', 'success');
        } else {
            showNotification('Failed to save settings', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error saving settings', 'error');
    }
});

// Model Settings Form
document.getElementById('model-settings-form')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const settings = {
        temperature: parseFloat(formData.get('temperature')),
        max_tokens: parseInt(formData.get('max_tokens'))
    };
    
    try {
        const response = await fetch('/admin/api/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        });
        
        if (response.ok) {
            showNotification('Model parameters updated!', 'success');
        } else {
            showNotification('Failed to update parameters', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error updating parameters', 'error');
    }
});

// Load conversations
async function loadConversations() {
    try {
        const response = await fetch('/admin/api/conversations');
        const conversations = await response.json();
        
        const listDiv = document.getElementById('conversations-list');
        
        if (conversations.length === 0) {
            listDiv.innerHTML = '<div class="empty-state"><p>No conversations yet</p></div>';
            return;
        }
        
        listDiv.innerHTML = conversations.reverse().map(conv => `
            <div class="conversation-item">
                <div class="conv-header">
                    <span class="conv-time">${new Date(conv.timestamp).toLocaleString()}</span>
                    <span class="conv-session">Session: ${conv.session_id.substring(0, 8)}</span>
                </div>
                <div class="conv-message user-msg">
                    <strong>User:</strong> ${escapeHtml(conv.user_message)}
                </div>
                <div class="conv-message bot-msg">
                    <strong>COLLIDE AI:</strong> ${escapeHtml(conv.bot_response.substring(0, 200))}${conv.bot_response.length > 200 ? '...' : ''}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading conversations:', error);
    }
}

// Export conversations
async function exportConversations() {
    try {
        const response = await fetch('/admin/api/conversations/export');
        const data = await response.json();
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `collide-conversations-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showNotification('Conversations exported!', 'success');
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error exporting conversations', 'error');
    }
}

// Clear conversations
async function clearConversations() {
    if (!confirm('Are you sure you want to clear all conversations? This cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch('/admin/api/conversations/clear', {
            method: 'POST'
        });
        
        if (response.ok) {
            showNotification('Conversations cleared!', 'success');
            loadConversations();
        } else {
            showNotification('Failed to clear conversations', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error clearing conversations', 'error');
    }
}

// Show notification
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#48bb78' : '#f56565'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

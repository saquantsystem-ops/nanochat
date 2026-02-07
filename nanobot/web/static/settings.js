// Settings page JavaScript

// Toggle section visibility
function toggleSection(channel) {
    const checkbox = document.getElementById(`${channel}-enabled`);
    const config = document.getElementById(`${channel}-config`);
    
    console.log(`Toggle ${channel}:`, checkbox.checked); // Debug
    
    if (checkbox && config) {
        config.style.display = checkbox.checked ? 'block' : 'none';
    } else {
        console.error(`Elements not found for ${channel}`);
    }
}

// Load settings on page load
window.addEventListener('DOMContentLoaded', () => {
    console.log('Settings page loaded'); // Debug
    
    loadAllSettings();
    checkGatewayStatus();
    
    // Add event listeners after page load
    const channels = ['telegram', 'whatsapp', 'discord', 'feishu'];
    channels.forEach(channel => {
        const checkbox = document.getElementById(`${channel}-enabled`);
        if (checkbox) {
            checkbox.addEventListener('change', () => toggleSection(channel));
            console.log(`Listener added for ${channel}`); // Debug
        }
    });
});

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Load all settings
async function loadAllSettings() {
    try {
        const response = await fetch('/api/settings');
        if (!response.ok) throw new Error('Failed to load settings');
        
        const data = await response.json();
        
        // Telegram
        if (data.telegram) {
            document.getElementById('telegram-enabled').checked = data.telegram.enabled;
            document.getElementById('telegram-token').value = data.telegram.token || '';
            document.getElementById('telegram-allowed').value = data.telegram.allowFrom?.join(', ') || '';
            document.getElementById('telegram-config').style.display = data.telegram.enabled ? 'block' : 'none';
            updateStatus('telegram', data.telegram.enabled);
        }
        
        // WhatsApp
        if (data.whatsapp) {
            document.getElementById('whatsapp-enabled').checked = data.whatsapp.enabled;
            document.getElementById('whatsapp-allowed').value = data.whatsapp.allowFrom?.join(', ') || '';
            document.getElementById('whatsapp-config').style.display = data.whatsapp.enabled ? 'block' : 'none';
            updateStatus('whatsapp', data.whatsapp.enabled);
        }
        
        // Discord
        if (data.discord) {
            document.getElementById('discord-enabled').checked = data.discord.enabled;
            document.getElementById('discord-token').value = data.discord.token || '';
            document.getElementById('discord-allowed').value = data.discord.allowFrom?.join(', ') || '';
            document.getElementById('discord-config').style.display = data.discord.enabled ? 'block' : 'none';
            updateStatus('discord', data.discord.enabled);
        }
        
        // Feishu
        if (data.feishu) {
            document.getElementById('feishu-enabled').checked = data.feishu.enabled;
            document.getElementById('feishu-appid').value = data.feishu.appId || '';
            document.getElementById('feishu-secret').value = data.feishu.appSecret || '';
            document.getElementById('feishu-allowed').value = data.feishu.allowFrom?.join(', ') || '';
            document.getElementById('feishu-config').style.display = data.feishu.enabled ? 'block' : 'none';
            updateStatus('feishu', data.feishu.enabled);
        }
        
    } catch (error) {
        console.error('Error loading settings:', error);
        showNotification('Failed to load settings', 'error');
    }
}

// Update status badge
function updateStatus(channel, connected) {
    const badge = document.getElementById(`${channel}-status`);
    if (connected) {
        badge.className = 'status-badge connected';
        badge.textContent = 'Connected';
    } else {
        badge.className = 'status-badge disconnected';
        badge.textContent = 'Disconnected';
    }
}

// Save Telegram settings
async function saveTelegram() {
    const enabled = document.getElementById('telegram-enabled').checked;
    const token = document.getElementById('telegram-token').value.trim();
    const allowFrom = document.getElementById('telegram-allowed').value
        .split(',')
        .map(id => id.trim())
        .filter(id => id);
    
    if (enabled && !token) {
        showNotification('Please enter a bot token', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/settings/telegram', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ enabled, token, allowFrom })
        });
        
        if (!response.ok) throw new Error('Failed to save settings');
        
        showNotification('✅ Telegram settings saved!', 'success');
        updateStatus('telegram', enabled);
    } catch (error) {
        showNotification('Failed to save Telegram settings', 'error');
    }
}

// Test Telegram connection
async function testTelegram() {
    try {
        const response = await fetch('/api/test/telegram');
        const data = await response.json();
        
        if (data.success) {
            showNotification('✅ Telegram connection successful!', 'success');
        } else {
            showNotification('❌ Telegram connection failed: ' + data.error, 'error');
        }
    } catch (error) {
        showNotification('Failed to test Telegram connection', 'error');
    }
}

// Save WhatsApp settings
async function saveWhatsApp() {
    const enabled = document.getElementById('whatsapp-enabled').checked;
    const allowFrom = document.getElementById('whatsapp-allowed').value
        .split(',')
        .map(num => num.trim())
        .filter(num => num);
    
    try {
        const response = await fetch('/api/settings/whatsapp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ enabled, allowFrom })
        });
        
        if (!response.ok) throw new Error('Failed to save settings');
        
        showNotification('✅ WhatsApp settings saved!', 'success');
        updateStatus('whatsapp', enabled);
    } catch (error) {
        showNotification('Failed to save WhatsApp settings', 'error');
    }
}

// Connect WhatsApp and show QR
async function connectWhatsApp() {
    const qrDiv = document.getElementById('whatsapp-qr');
    qrDiv.style.display = 'block';
    
    try {
        const response = await fetch('/api/whatsapp/qr');
        const data = await response.json();
        
        if (data.qr) {
            qrDiv.innerHTML = `
                <div class="qr-code">
                    <img src="${data.qr}" alt="WhatsApp QR Code">
                    <p style="color: #666; margin-top: 12px;">Scan this QR code with WhatsApp</p>
                </div>
            `;
        } else if (data.command) {
            // Show terminal instructions
            qrDiv.innerHTML = `
                <div style="background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 8px; padding: 20px; margin: 16px 0;">
                    <h4 style="color: #e3e3e3; margin-bottom: 12px;">📱 WhatsApp Connection Steps</h4>
                    <p style="color: #888; margin-bottom: 16px;">${data.message}</p>
                    
                    <div style="background: #0f0f0f; padding: 12px; border-radius: 6px; margin-bottom: 16px;">
                        <code style="color: #10b981; font-family: monospace;">${data.command}</code>
                    </div>
                    
                    <ol style="color: #888; font-size: 13px; line-height: 1.8; padding-left: 20px;">
                        ${data.instructions.map(inst => `<li>${inst}</li>`).join('')}
                    </ol>
                    
                    <div style="margin-top: 16px; padding: 12px; background: #2a2a2a; border-radius: 6px;">
                        <p style="color: #888; font-size: 12px; margin: 0;">
                            <strong style="color: #e3e3e3;">💡 Tip:</strong> Keep the terminal window open while using WhatsApp. 
                            The QR code will appear in the terminal, not in this web UI.
                        </p>
                    </div>
                    
                    <button class="btn btn-secondary" onclick="document.getElementById('whatsapp-qr').style.display='none'" style="margin-top: 16px; width: 100%;">
                        Close
                    </button>
                </div>
            `;
        } else {
            showNotification(data.error || 'Failed to generate QR code', 'error');
            qrDiv.style.display = 'none';
        }
    } catch (error) {
        showNotification('Failed to connect WhatsApp: ' + error.message, 'error');
        qrDiv.style.display = 'none';
    }
}

// Save Discord settings
async function saveDiscord() {
    const enabled = document.getElementById('discord-enabled').checked;
    const token = document.getElementById('discord-token').value.trim();
    const allowFrom = document.getElementById('discord-allowed').value
        .split(',')
        .map(id => id.trim())
        .filter(id => id);
    
    if (enabled && !token) {
        showNotification('Please enter a bot token', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/settings/discord', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ enabled, token, allowFrom })
        });
        
        if (!response.ok) throw new Error('Failed to save settings');
        
        showNotification('✅ Discord settings saved!', 'success');
        updateStatus('discord', enabled);
    } catch (error) {
        showNotification('Failed to save Discord settings', 'error');
    }
}

// Test Discord connection
async function testDiscord() {
    try {
        const response = await fetch('/api/test/discord');
        const data = await response.json();
        
        if (data.success) {
            showNotification('✅ Discord connection successful!', 'success');
        } else {
            showNotification('❌ Discord connection failed: ' + data.error, 'error');
        }
    } catch (error) {
        showNotification('Failed to test Discord connection', 'error');
    }
}

// Save Feishu settings
async function saveFeishu() {
    const enabled = document.getElementById('feishu-enabled').checked;
    const appId = document.getElementById('feishu-appid').value.trim();
    const appSecret = document.getElementById('feishu-secret').value.trim();
    const allowFrom = document.getElementById('feishu-allowed').value
        .split(',')
        .map(id => id.trim())
        .filter(id => id);
    
    if (enabled && (!appId || !appSecret)) {
        showNotification('Please enter App ID and App Secret', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/settings/feishu', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ enabled, appId, appSecret, allowFrom })
        });
        
        if (!response.ok) throw new Error('Failed to save settings');
        
        showNotification('✅ Feishu settings saved!', 'success');
        updateStatus('feishu', enabled);
    } catch (error) {
        showNotification('Failed to save Feishu settings', 'error');
    }
}

// Test Feishu connection
async function testFeishu() {
    try {
        const response = await fetch('/api/test/feishu');
        const data = await response.json();
        
        if (data.success) {
            showNotification('✅ Feishu connection successful!', 'success');
        } else {
            showNotification('❌ Feishu connection failed: ' + data.error, 'error');
        }
    } catch (error) {
        showNotification('Failed to test Feishu connection', 'error');
    }
}

// Gateway control
function copyGatewayCommand() {
    const command = 'nanobot gateway';
    navigator.clipboard.writeText(command).then(() => {
        showNotification('✅ Command copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('❌ Failed to copy command', 'error');
    });
}

async function startGateway() {
    showNotification('ℹ️ Please run "nanobot gateway" in a terminal', 'info');
}

async function stopGateway() {
    showNotification('ℹ️ Press Ctrl+C in the gateway terminal to stop', 'info');
}

async function checkGatewayStatus() {
    try {
        const response = await fetch('/api/gateway/status');
        const data = await response.json();
        
        updateGatewayStatus(data.status);
    } catch (error) {
        console.error('Failed to check gateway status:', error);
    }
}

function updateGatewayStatus(status) {
    const badge = document.getElementById('gateway-status');
    if (status === 'running') {
        badge.className = 'status-badge connected';
        badge.textContent = 'Running';
    } else {
        badge.className = 'status-badge disconnected';
        badge.textContent = 'Stopped';
    }
}

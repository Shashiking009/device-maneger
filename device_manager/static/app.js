let currentSessionId = null;
let isGenerating = false;

// DOM Elements
const sessionsListEl = document.getElementById('sessions-list');
const docsSidebarListEl = document.getElementById('docs-sidebar-list');
const chatMessagesEl = document.getElementById('chat-messages');
const userInputEl = document.getElementById('user-input');
const btnSend = document.getElementById('btn-send');
const btnNewChat = document.getElementById('btn-new-chat');
const btnClearChat = document.getElementById('btn-clear-chat');
const welcomeCard = document.getElementById('welcome-card');
const currentChatTitle = document.getElementById('current-chat-title');
const activeModelName = document.getElementById('active-model-name');
const ollamaStatusDot = document.getElementById('ollama-status-dot');

// Metrics
const metricCpuVal = document.getElementById('metric-cpu-val');
const metricRamVal = document.getElementById('metric-ram-val');
const progressCpu = document.getElementById('progress-cpu');
const progressRam = document.getElementById('progress-ram');

// Controls
const toggleRag = document.getElementById('toggle-rag');
const inputTemp = document.getElementById('input-temp');
const tempVal = document.getElementById('temp-val');

// Modals
const ragModal = document.getElementById('rag-modal');
const btnOpenRagModal = document.getElementById('btn-open-rag-modal');
const btnCloseRagModal = document.getElementById('btn-close-rag-modal');
const fileInput = document.getElementById('file-input');
const uploadDropzone = document.getElementById('upload-dropzone');
const modalDocsList = document.getElementById('modal-docs-list');

const systemModal = document.getElementById('system-modal');
const btnSystemModal = document.getElementById('btn-system-modal');
const btnCloseSysModal = document.getElementById('btn-close-sys-modal');

// Spidy Voice Assistant Elements
const btnSpidyVoice = document.getElementById('btn-spidy-voice');
const spidyBanner = document.getElementById('spidy-banner');
const btnCloseSpidy = document.getElementById('btn-close-spidy');
const spidyTitle = document.getElementById('spidy-title');
const spidySub = document.getElementById('spidy-sub');

let recognition = null;
let isSpidyActive = false;

// Init
document.addEventListener('DOMContentLoaded', () => {
    initApp();
    setupEventListeners();
    initSpidyVoice();
});

async function initApp() {
    await fetchSessions();
    await fetchDocuments();
    fetchSystemMetrics();
    setInterval(fetchSystemMetrics, 4000);
}

function setupEventListeners() {
    btnNewChat.addEventListener('click', createNewSession);
    btnClearChat.addEventListener('click', clearCurrentChat);
    btnSend.addEventListener('click', sendMessage);

    userInputEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    userInputEl.addEventListener('input', () => {
        userInputEl.style.height = 'auto';
        userInputEl.style.height = Math.min(userInputEl.scrollHeight, 140) + 'px';
    });

    inputTemp.addEventListener('input', (e) => {
        tempVal.textContent = e.target.value;
    });

    // Quick Prompts
    document.querySelectorAll('.prompt-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const promptText = chip.getAttribute('data-prompt');
            userInputEl.value = promptText;
            sendMessage();
        });
    });

    // Modals
    btnOpenRagModal.addEventListener('click', () => {
        ragModal.classList.remove('hidden');
        renderModalDocs();
    });
    btnCloseRagModal.addEventListener('click', () => ragModal.classList.add('hidden'));

    btnSystemModal.addEventListener('click', () => {
        systemModal.classList.remove('hidden');
        updateDiagnosticsModal();
    });
    btnCloseSysModal.addEventListener('click', () => systemModal.classList.add('hidden'));

    // File Upload
    document.getElementById('btn-attach-file').addEventListener('click', () => fileInput.click());
    uploadDropzone.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', (e) => handleFileUpload(e.target.files));

    uploadDropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadDropzone.classList.add('dragover');
    });
    uploadDropzone.addEventListener('dragleave', () => uploadDropzone.classList.remove('dragover'));
    uploadDropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadDropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFileUpload(e.dataTransfer.files);
        }
    });
}

// System Metrics
async function fetchSystemMetrics() {
    try {
        const res = await fetch('/api/system');
        if (res.ok) {
            const data = await res.json();
            metricCpuVal.textContent = `${data.cpu.percent}%`;
            progressCpu.style.width = `${data.cpu.percent}%`;

            metricRamVal.textContent = `${data.memory.used_gb} / ${data.memory.total_gb} GB`;
            progressRam.style.width = `${data.memory.percent}%`;

            if (data.ollama.online) {
                ollamaStatusDot.className = 'status-dot dot-online';
                ollamaStatusDot.title = 'Ollama Engine Online';
                activeModelName.textContent = data.ollama.active_model || 'qwen3:1.7b';
            } else {
                ollamaStatusDot.className = 'status-dot dot-offline';
                ollamaStatusDot.title = 'Ollama Offline';
            }
        }
    } catch (e) {
        console.error("Metrics fetch error:", e);
    }
}

// Sessions
async function fetchSessions() {
    try {
        const res = await fetch('/api/sessions');
        if (res.ok) {
            const sessions = await res.json();
            renderSessions(sessions);
            if (sessions.length > 0 && !currentSessionId) {
                switchSession(sessions[0].id, sessions[0].title);
            } else if (sessions.length === 0) {
                createNewSession();
            }
        }
    } catch (e) {
        console.error("Sessions fetch error:", e);
    }
}

function renderSessions(sessions) {
    if (sessions.length === 0) {
        sessionsListEl.innerHTML = '<li class="empty-state">No conversations yet</li>';
        return;
    }
    sessionsListEl.innerHTML = sessions.map(s => `
        <li class="session-item ${s.id === currentSessionId ? 'active' : ''}" data-id="${s.id}" onclick="switchSession('${s.id}', '${escapeHtml(s.title)}')">
            <span class="session-title-text"><i class="fa-regular fa-message"></i> ${escapeHtml(s.title)}</span>
            <i class="fa-solid fa-xmark btn-delete-session" onclick="event.stopPropagation(); deleteSession('${s.id}')"></i>
        </li>
    `).join('');
}

async function createNewSession() {
    try {
        const res = await fetch('/api/sessions', { method: 'POST' });
        if (res.ok) {
            const newSess = await res.json();
            currentSessionId = newSess.id;
            await fetchSessions();
            switchSession(newSess.id, newSess.title);
        }
    } catch (e) {
        console.error("Create session error:", e);
    }
}

async function deleteSession(id) {
    try {
        await fetch(`/api/sessions/${id}`, { method: 'DELETE' });
        if (currentSessionId === id) currentSessionId = null;
        await fetchSessions();
    } catch (e) {
        console.error("Delete session error:", e);
    }
}

async function switchSession(id, title) {
    currentSessionId = id;
    currentChatTitle.textContent = title || "Conversation";
    
    // Highlight active item
    document.querySelectorAll('.session-item').forEach(el => {
        el.classList.toggle('active', el.getAttribute('data-id') === id);
    });

    // Load messages
    try {
        const res = await fetch(`/api/sessions/${id}/messages`);
        if (res.ok) {
            const msgs = await res.json();
            renderMessages(msgs);
        }
    } catch (e) {
        console.error("Fetch messages error:", e);
    }
}

function clearCurrentChat() {
    chatMessagesEl.innerHTML = '';
    chatMessagesEl.appendChild(welcomeCard);
    welcomeCard.style.display = 'block';
}

function renderMessages(msgs) {
    chatMessagesEl.innerHTML = '';
    if (msgs.length === 0) {
        chatMessagesEl.appendChild(welcomeCard);
        welcomeCard.style.display = 'block';
        return;
    }
    welcomeCard.style.display = 'none';

    msgs.forEach(m => {
        appendMessageUI(m.role, m.content, m.sources, m.tokens_per_sec);
    });
    chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
}

// Chat Flow
async function sendMessage() {
    const text = userInputEl.value.trim();
    if (!text || isGenerating) return;

    if (!currentSessionId) {
        await createNewSession();
    }

    welcomeCard.style.display = 'none';
    appendMessageUI('user', text);
    userInputEl.value = '';
    userInputEl.style.height = 'auto';

    isGenerating = true;
    btnSend.disabled = true;

    const assistantBubble = appendMessageUI('assistant', '<i class="fa-solid fa-spinner fa-spin"></i> Generating...');
    let fullText = '';
    let sourcesList = [];

    try {
        const response = await fetch('/api/chat/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: currentSessionId,
                message: text,
                use_rag: toggleRag.checked,
                temperature: parseFloat(inputTemp.value)
            })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startswith('data: ') || line.indexOf('data: ') === 0) {
                    const jsonStr = line.replace('data: ', '').trim();
                    if (!jsonStr) continue;
                    try {
                        const data = JSON.parse(jsonStr);
                        if (data.type === 'sources') {
                            sourcesList = data.sources;
                        } else if (data.type === 'token') {
                            fullText += data.token;
                            updateAssistantBubble(assistantBubble, fullText, sourcesList);
                        } else if (data.type === 'done') {
                            updateAssistantBubble(assistantBubble, data.full_response || fullText, sourcesList, data.tps);
                        }
                    } catch (e) {}
                }
            }
        }
    } catch (e) {
        updateAssistantBubble(assistantBubble, `[Stream Error]: ${e.message}`, []);
    } finally {
        isGenerating = false;
        btnSend.disabled = false;
        fetchSessions();
    }
}

function appendMessageUI(role, content, sources = [], tps = null) {
    const row = document.createElement('div');
    row.className = `msg-row ${role}-msg`;

    const icon = role === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';
    
    let formattedContent = role === 'assistant' && typeof marked !== 'undefined' ? marked.parse(content) : escapeHtml(content);

    let sourcesHtml = '';
    if (sources && sources.length > 0) {
        sourcesHtml = `<div class="sources-box">
            <strong>Sources:</strong> ${sources.map(s => `<span class="source-tag"><i class="fa-solid fa-file-lines"></i> ${escapeHtml(s.filename)}</span>`).join('')}
        </div>`;
    }

    let tpsHtml = tps ? `<div class="tps-badge"><i class="fa-solid fa-bolt"></i> ${tps} tok/s</div>` : '';

    row.innerHTML = `
        <div class="avatar">${icon}</div>
        <div class="msg-bubble">
            <div class="msg-content">${formattedContent}</div>
            ${sourcesHtml}
            ${tpsHtml}
        </div>
    `;

    chatMessagesEl.appendChild(row);
    chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;

    // Apply syntax highlighting
    if (role === 'assistant' && typeof hljs !== 'undefined') {
        row.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
    }

    return row.querySelector('.msg-content');
}

function updateAssistantBubble(contentEl, text, sources = [], tps = null) {
    contentEl.innerHTML = typeof marked !== 'undefined' ? marked.parse(text) : escapeHtml(text);
    
    // Parent bubble elements update
    const bubble = contentEl.closest('.msg-bubble');
    if (sources && sources.length > 0 && !bubble.querySelector('.sources-box')) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'sources-box';
        sourcesDiv.innerHTML = `<strong>Sources:</strong> ${sources.map(s => `<span class="source-tag"><i class="fa-solid fa-file-lines"></i> ${escapeHtml(s.filename)}</span>`).join('')}`;
        bubble.appendChild(sourcesDiv);
    }
    
    if (tps && !bubble.querySelector('.tps-badge')) {
        const tpsDiv = document.createElement('div');
        tpsDiv.className = 'tps-badge';
        tpsDiv.innerHTML = `<i class="fa-solid fa-bolt"></i> ${tps} tok/s`;
        bubble.appendChild(tpsDiv);
    }

    chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
    if (typeof hljs !== 'undefined') {
        contentEl.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
    }
}

// RAG Documents
async function fetchDocuments() {
    try {
        const res = await fetch('/api/documents');
        if (res.ok) {
            const docs = await res.json();
            renderDocumentsSidebar(docs);
        }
    } catch (e) {
        console.error("Docs fetch error:", e);
    }
}

function renderDocumentsSidebar(docs) {
    if (docs.length === 0) {
        docsSidebarListEl.innerHTML = '<li class="empty-state">No local documents indexed</li>';
        return;
    }
    docsSidebarListEl.innerHTML = docs.map(d => `
        <li class="doc-item">
            <span><i class="fa-solid fa-file-code"></i> ${escapeHtml(d.filename)}</span>
            <i class="fa-solid fa-trash-can btn-delete-doc" onclick="deleteDocument(${d.id})"></i>
        </li>
    `).join('');
}

async function renderModalDocs() {
    try {
        const res = await fetch('/api/documents');
        if (res.ok) {
            const docs = await res.json();
            if (docs.length === 0) {
                modalDocsList.innerHTML = '<p class="empty-state">No documents added yet.</p>';
                return;
            }
            modalDocsList.innerHTML = docs.map(d => `
                <div class="doc-item" style="margin-bottom:6px;">
                    <div>
                        <strong>${escapeHtml(d.filename)}</strong>
                        <div style="font-size:0.75rem; color:#9ca3af;">${d.chunks_count} chunks | ${(d.file_size/1024).toFixed(1)} KB</div>
                    </div>
                    <button class="btn-icon-small" onclick="deleteDocument(${d.id})"><i class="fa-solid fa-trash text-rose"></i></button>
                </div>
            `).join('');
        }
    } catch (e) {
        modalDocsList.innerHTML = '<p class="empty-state">Error loading documents.</p>';
    }
}

async function handleFileUpload(files) {
    for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);
        try {
            const res = await fetch('/api/documents/upload', {
                method: 'POST',
                body: formData
            });
            if (res.ok) {
                await fetchDocuments();
                renderModalDocs();
            }
        } catch (e) {
            console.error("Upload error:", e);
        }
    }
}

async function deleteDocument(id) {
    try {
        await fetch(`/api/documents/${id}`, { method: 'DELETE' });
        await fetchDocuments();
        renderModalDocs();
    } catch (e) {
        console.error("Delete doc error:", e);
    }
}

// System Diagnostics Modal
async function updateDiagnosticsModal() {
    const diagOs = document.getElementById('diag-os');
    const diagCpu = document.getElementById('diag-cpu-cores');
    const diagRam = document.getElementById('diag-ram-total');
    const diagDisk = document.getElementById('diag-disk-total');
    const ollamaBox = document.getElementById('ollama-info-box');

    try {
        const res = await fetch('/api/system');
        if (res.ok) {
            const d = await res.json();
            diagOs.textContent = d.os;
            diagCpu.textContent = `${d.cpu.cores} Logical Cores (${d.cpu.freq_mhz} MHz)`;
            diagRam.textContent = `${d.memory.total_gb} GB (${d.memory.percent}% Used)`;
            diagDisk.textContent = `${d.disk.total_gb} GB (${d.disk.percent}% Used)`;

            ollamaBox.innerHTML = `
                Status: ${d.ollama.online ? 'ONLINE' : 'OFFLINE'}<br>
                Active Model: ${d.ollama.active_model}<br>
                Available Models: ${d.ollama.available_models.join(', ') || 'None'}<br>
                Engine URL: http://localhost:11434
            `;
        }
    } catch (e) {
        ollamaBox.textContent = "Error reading system metrics.";
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

// ==================== SPIDY VOICE ASSISTANT ENGINE ====================
function initSpidyVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        btnSpidyVoice.title = "Browser does not support Speech Recognition";
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    btnSpidyVoice.addEventListener('click', toggleSpidyVoice);
    btnCloseSpidy.addEventListener('click', stopSpidyVoice);

    recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            transcript += event.results[i][0].transcript;
        }

        const lowerTranscript = transcript.lowerCase ? transcript.lowerCase() : transcript.toLowerCase();
        
        // Wake Word Detection: "spidy", "spidey", "spider"
        if (lowerTranscript.includes('spidy') || lowerTranscript.includes('spidey') || lowerTranscript.includes('spider')) {
            showSpidyBanner('🕷️ Spidy Activated!', `Heard: "${transcript}"`);
            
            if (event.results[event.resultIndex].isFinal) {
                processSpidyVoiceCommand(transcript);
            }
        } else {
            spidySub.textContent = `Listening... ${transcript}`;
        }
    };

    recognition.onerror = (err) => {
        console.warn("Spidy Speech Recognition Error:", err);
    };

    recognition.onend = () => {
        if (isSpidyActive) {
            try { recognition.start(); } catch (e) {}
        }
    };
}

function toggleSpidyVoice() {
    if (isSpidyActive) {
        stopSpidyVoice();
    } else {
        startSpidyVoice();
    }
}

function startSpidyVoice() {
    if (!recognition) return;
    isSpidyActive = true;
    btnSpidyVoice.classList.add('listening');
    spidyBanner.classList.remove('hidden');
    spidyTitle.textContent = '🕷️ Spidy Listening...';
    spidySub.textContent = 'Say "Hey Spidy open calculator", "Hey Spidy open downloads", or "Hey Spidy open notepad"';
    try { recognition.start(); } catch (e) {}
    speakText("Spidy Voice Assistant active. Say Hey Spidy followed by your command.");
}

function stopSpidyVoice() {
    isSpidyActive = false;
    btnSpidyVoice.classList.remove('listening');
    spidyBanner.classList.add('hidden');
    if (recognition) {
        try { recognition.stop(); } catch (e) {}
    }
}

function showSpidyBanner(title, sub) {
    spidyBanner.classList.remove('hidden');
    spidyTitle.textContent = title;
    spidySub.textContent = sub;
}

async function processSpidyVoiceCommand(commandText) {
    spidySub.textContent = `Executing: "${commandText}"...`;
    
    try {
        const res = await fetch('/api/voice/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: commandText })
        });

        if (res.ok) {
            const data = await res.json();
            
            if (data.action === 'open_app' || data.action === 'close_app' || data.action === 'open_folder' || data.action === 'open_file') {
                speakText(data.message);
                showSpidyBanner('⚡ Task Executed', data.message);
                appendMessageUI('assistant', `**[Spidy Action]** ${data.message}`);
            } else if (data.status === 'ai_query') {
                speakText(`Processing query: ${data.query}`);
                userInputEl.value = data.query;
                sendMessage();
            } else {
                speakText(data.message);
                showSpidyBanner('🕷️ Spidy', data.message);
            }
        }
    } catch (e) {
        speakText("Sorry, I encountered an error processing your voice command.");
    }
}

function speakText(text) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel(); // Stop any ongoing speech
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
}


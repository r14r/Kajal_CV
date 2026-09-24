const $ = id => document.getElementById(id);
let conversationId = null;
const messages = $('messages');

async function api(path, options = {}) {
  const response = await fetch(path, options);
  const body = await response.json();
  if (!response.ok) throw new Error(typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail || 'Request failed'));
  return body;
}
function clearWelcome() { const welcome = messages.querySelector('.welcome'); if (welcome) welcome.remove(); }
function addMessage(role, content, citations = []) {
  clearWelcome();
  const row = document.createElement('article'); row.className = 'message ' + role;
  const avatar = document.createElement('div'); avatar.className = 'avatar'; avatar.textContent = role === 'user' ? 'U' : '✦';
  const body = document.createElement('div'); body.className = 'bubble'; body.textContent = content;
  if (citations.length) {
    const details = document.createElement('details'); details.className = 'sources';
    const summary = document.createElement('summary'); summary.textContent = `View ${citations.length} source passage${citations.length === 1 ? '' : 's'}`; details.append(summary);
    citations.forEach(item => { const block = document.createElement('div'); block.className = 'source';
      const heading = document.createElement('strong'); heading.textContent = `[${item.number}] ${item.document}, passage ${item.passage}`;
      const excerpt = document.createElement('p'); excerpt.textContent = item.excerpt; block.append(heading, excerpt); details.append(block); });
    body.append(details);
  }
  row.append(avatar, body); messages.append(row); $('chatPanel').scrollTop = $('chatPanel').scrollHeight;
}
function newChat() { conversationId = null; messages.replaceChildren(); const welcome = document.createElement('div'); welcome.className = 'welcome';
  welcome.innerHTML = '<div class="spark">✦</div><h1>New conversation</h1><p>Ask a question about your knowledge library.</p>'; messages.append(welcome);
  document.querySelectorAll('.history').forEach(el => el.classList.remove('active')); $('question').focus(); closeSidebar(); }
async function loadConversations() { const chats = await api('/api/conversations'); const list = $('conversationList'); list.replaceChildren();
  chats.forEach(chat => { const button = document.createElement('button'); button.type = 'button'; button.className = 'history' + (chat.id === conversationId ? ' active' : '');
    button.textContent = chat.title; button.onclick = () => openConversation(chat.id); list.append(button); }); }
async function openConversation(id) { try { const chat = await api('/api/conversations/' + id); conversationId = id; messages.replaceChildren();
  chat.messages.forEach(message => addMessage(message.role, message.content, message.citations)); await loadConversations(); closeSidebar(); } catch (error) { $('error').textContent = error.message; } }
function closeSidebar() { $('sidebar').classList.remove('open'); }
async function send(question) { $('error').textContent = ''; const button = $('sendButton'); button.disabled = true; addMessage('user', question);
  try { const response = await api('/api/chat', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({question, conversation_id:conversationId}) });
    conversationId = response.conversation_id; addMessage('assistant', response.answer, response.citations); await loadConversations();
  } catch(error) { $('error').textContent = error.message; addMessage('assistant', 'Request failed. Your message was not saved.'); } finally { button.disabled = false; $('question').focus(); } }
$('chatForm').addEventListener('submit', event => { event.preventDefault(); const question = $('question').value.trim(); if (!question) return; $('question').value = ''; send(question); });
$('question').addEventListener('keydown', event => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); $('chatForm').requestSubmit(); } });
document.querySelectorAll('[data-question]').forEach(button => button.onclick = () => { $('question').value = button.dataset.question; $('chatForm').requestSubmit(); });
$('newChat').onclick = newChat; $('menuButton').onclick = () => $('sidebar').classList.toggle('open');
$('showDocs').onclick = () => { closeSidebar(); $('docsDialog').showModal(); loadDocuments(); }; $('closeDocs').onclick = () => $('docsDialog').close();
async function loadDocuments() { try { const docs = await api('/api/documents'); const list = $('documentList'); list.replaceChildren();
  docs.forEach(doc => { const li = document.createElement('li'); const label = document.createElement('span'); label.textContent = `${doc.title} (${doc.characters} characters)`;
    const remove = document.createElement('button'); remove.type = 'button'; remove.textContent = 'Delete'; remove.setAttribute('aria-label', 'Delete ' + doc.title);
    remove.onclick = async () => { if (!confirm('Delete this document?')) return; try { await api('/api/documents/' + doc.id, {method:'DELETE'}); await loadDocuments(); } catch(error) { $('docError').textContent = error.message; } };
    li.append(label, remove); list.append(li); }); } catch(error) { $('docError').textContent = error.message; } }
$('docFile').addEventListener('change', async event => { const file = event.target.files[0]; if (!file) return;
  if (!/\.(txt|md)$/i.test(file.name) || file.size > 65536) { $('docError').textContent = 'Choose a .txt or .md file up to 64 KiB.'; return; }
  $('docTitle').value = file.name; $('docContent').value = await file.text(); $('docError').textContent = ''; });
$('documentForm').addEventListener('submit', async event => { event.preventDefault(); $('docError').textContent = '';
  try { await api('/api/documents', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({title:$('docTitle').value, content:$('docContent').value})});
    $('documentForm').reset(); await loadDocuments(); } catch(error) { $('docError').textContent = error.message; } });
loadConversations().catch(error => { $('error').textContent = error.message; });

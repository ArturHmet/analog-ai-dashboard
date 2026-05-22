(function(){
  const GOLD='#F59E0B', GOLD_DARK='#D97706', BG='#111827', CARD='#1F2937', BORDER='#374151';
  const css=`
#ph-chat-btn{position:fixed;bottom:24px;right:24px;z-index:10000;width:58px;height:58px;border-radius:50%;background:${GOLD};color:#000;border:none;cursor:pointer;box-shadow:0 4px 20px rgba(245,158,11,.45);font-size:22px;display:flex;align-items:center;justify-content:center;transition:transform .2s,box-shadow .2s}
#ph-chat-btn:hover{transform:scale(1.08);box-shadow:0 6px 28px rgba(245,158,11,.6)}
#ph-chat-btn .ph-btn-dot{position:absolute;top:4px;right:4px;width:10px;height:10px;background:#10B981;border-radius:50%;border:2px solid #000}
#ph-chat-box{position:fixed;bottom:96px;right:24px;z-index:10000;width:348px;max-width:calc(100vw - 32px);background:${BG};border:1px solid ${BORDER};border-radius:18px;box-shadow:0 12px 48px rgba(0,0,0,.55);display:none;flex-direction:column;overflow:hidden;font-family:'Inter','Plus Jakarta Sans',system-ui,sans-serif;animation:ph-slide-up .25s ease}
@keyframes ph-slide-up{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
#ph-chat-header{background:linear-gradient(135deg,${GOLD_DARK},${GOLD});color:#000;padding:14px 16px;display:flex;justify-content:space-between;align-items:center}
#ph-chat-header .ph-header-info{display:flex;align-items:center;gap:10px}
#ph-chat-header .ph-avatar{width:34px;height:34px;border-radius:50%;background:rgba(0,0,0,.2);display:flex;align-items:center;justify-content:center;font-size:16px}
#ph-chat-header .ph-title{font-weight:700;font-size:14px;line-height:1.2}
#ph-chat-header .ph-subtitle{font-size:11px;opacity:.75;margin-top:1px}
#ph-close{font-size:18px;cursor:pointer;opacity:.7;background:none;border:none;color:#000;line-height:1;padding:2px}
#ph-close:hover{opacity:1}
#ph-chat-messages{flex:1;padding:14px 12px;overflow-y:auto;max-height:300px;display:flex;flex-direction:column;gap:10px;scrollbar-width:thin;scrollbar-color:${BORDER} transparent}
#ph-chat-messages::-webkit-scrollbar{width:4px}
#ph-chat-messages::-webkit-scrollbar-thumb{background:${BORDER};border-radius:2px}
.ph-msg{max-width:86%;padding:10px 13px;border-radius:14px;font-size:13.5px;line-height:1.5;word-break:break-word}
.ph-msg.bot{background:${CARD};color:#E5E7EB;align-self:flex-start;border-bottom-left-radius:4px;border:1px solid ${BORDER}}
.ph-msg.user{background:${GOLD};color:#000;align-self:flex-end;border-bottom-right-radius:4px;font-weight:500}
.ph-typing{display:flex;gap:5px;padding:10px 13px;background:${CARD};border-radius:14px;border-bottom-left-radius:4px;width:fit-content;align-self:flex-start;border:1px solid ${BORDER}}
.ph-typing span{width:7px;height:7px;background:#6B7280;border-radius:50%;animation:ph-bounce .9s infinite}
.ph-typing span:nth-child(2){animation-delay:.18s}.ph-typing span:nth-child(3){animation-delay:.36s}
@keyframes ph-bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-7px)}}
.ph-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:2px}
.ph-chip{background:transparent;border:1px solid ${GOLD};color:${GOLD};border-radius:20px;padding:4px 11px;font-size:12px;cursor:pointer;transition:all .15s;font-family:inherit}
.ph-chip:hover{background:${GOLD};color:#000}
#ph-chat-input-row{display:flex;border-top:1px solid ${BORDER};padding:10px 12px;gap:8px;align-items:center}
#ph-chat-input{flex:1;background:${CARD};border:1px solid ${BORDER};border-radius:10px;outline:none;font-size:13.5px;padding:8px 12px;font-family:inherit;color:#E5E7EB;transition:border-color .15s}
#ph-chat-input:focus{border-color:${GOLD}}
#ph-chat-input::placeholder{color:#6B7280}
#ph-chat-send{background:${GOLD};color:#000;border:none;border-radius:10px;padding:8px 14px;cursor:pointer;font-size:13px;font-weight:700;transition:background .15s;flex-shrink:0}
#ph-chat-send:hover{background:${GOLD_DARK}}
`;
  const style=document.createElement('style');style.textContent=css;document.head.appendChild(style);

  const btn=document.createElement('button');btn.id='ph-chat-btn';
  btn.innerHTML='🤖<div class="ph-btn-dot"></div>';
  document.body.appendChild(btn);

  const box=document.createElement('div');box.id='ph-chat-box';
  box.innerHTML=`
<div id="ph-chat-header">
  <div class="ph-header-info">
    <div class="ph-avatar">🤖</div>
    <div><div class="ph-title">ProHelp AI</div><div class="ph-subtitle">Usually replies instantly</div></div>
  </div>
  <button id="ph-close">✕</button>
</div>
<div id="ph-chat-messages">
  <div class="ph-msg bot">Hi! I'm your ProHelp AI assistant 👋<br>I can help you find services, post a task, or answer any questions.</div>
  <div class="ph-chips">
    <button class="ph-chip" onclick="phQuick('How do I post a task?')">Post a task</button>
    <button class="ph-chip" onclick="phQuick('What services are available?')">Services</button>
    <button class="ph-chip" onclick="phQuick('How does payment work?')">Payment</button>
  </div>
</div>
<div id="ph-chat-input-row">
  <input id="ph-chat-input" placeholder="Ask anything..." maxlength="400"/>
  <button id="ph-chat-send">Send</button>
</div>`;
  document.body.appendChild(box);

  let history=[], open=false;
  btn.onclick=()=>{open=!open;box.style.display=open?'flex':'none';if(open)document.getElementById('ph-chat-input').focus()};
  document.getElementById('ph-close').onclick=()=>{open=false;box.style.display='none'};

  window.phQuick=function(msg){
    document.getElementById('ph-chat-input').value=msg;
    phSend();
  };

  async function phSend(){
    const inp=document.getElementById('ph-chat-input');
    const msg=inp.value.trim();if(!msg)return;
    inp.value='';
    const msgs=document.getElementById('ph-chat-messages');
    // remove chips if present
    const chips=msgs.querySelector('.ph-chips');if(chips)chips.remove();
    msgs.innerHTML+=`<div class="ph-msg user">${msg.replace(/</g,'&lt;')}</div>`;
    msgs.innerHTML+=`<div class="ph-typing" id="ph-typing"><span></span><span></span><span></span></div>`;
    msgs.scrollTop=msgs.scrollHeight;
    history.push({role:'user',content:msg});
    try{
      const r=await fetch('/api/chatbot/message',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg,history:history.slice(-8)})});
      const d=await r.json();
      document.getElementById('ph-typing')?.remove();
      const reply=(d.reply||d.response||d.message||d.text||'Let me connect you with our team.').replace(/</g,'&lt;');
      msgs.innerHTML+=`<div class="ph-msg bot">${reply}</div>`;
      history.push({role:'assistant',content:reply});
    }catch(e){
      document.getElementById('ph-typing')?.remove();
      msgs.innerHTML+=`<div class="ph-msg bot">I'm having a moment — please try again or <a href="/register.html" style="color:#F59E0B">browse tasks</a>.</div>`;
    }
    msgs.scrollTop=msgs.scrollHeight;
  }
  document.getElementById('ph-chat-send').onclick=phSend;
  document.getElementById('ph-chat-input').onkeydown=e=>{if(e.key==='Enter'&&!e.shiftKey)phSend()};
})();

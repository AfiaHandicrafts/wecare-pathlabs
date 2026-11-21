(function () {
  const ENABLE_GOOGLE = false;

  function boot() {
    const sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

    function el(tag, text, css) {
      const e = document.createElement(tag);
      if (text) e.textContent = text;
      if (css) e.style.cssText = css;
      return e;
    }
    const inputCss = 'padding:10px;border:1px solid #ccc;border-radius:8px;font-size:16px;width:100%;box-sizing:border-box';
    const btnCss = 'padding:10px;border:0;border-radius:8px;background:#0a7;color:#fff;font-size:16px;cursor:pointer';
    const linkCss = 'background:none;border:0;color:#555;cursor:pointer;font-size:15px';

    const overlay = el('div', '', 'display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;align-items:center;justify-content:center;padding:16px');
    const card = el('div', '', 'background:#fff;color:#222;max-width:380px;width:100%;border-radius:12px;padding:20px;font-family:sans-serif;display:flex;flex-direction:column;gap:10px;max-height:90vh;overflow:auto');
    overlay.appendChild(card);
    document.body.appendChild(overlay);

    function close() { overlay.style.display = 'none'; }

    function showLogin(note) {
      card.replaceChildren();
      card.append(el('h3', 'Login to send a message', 'margin:0'));
      if (note) card.append(el('p', note, 'margin:0;color:#555'));
      if (ENABLE_GOOGLE) {
        const g = el('button', 'Continue with Google', btnCss);
        g.onclick = () => sb.auth.signInWithOAuth({
          provider: 'google',
          options: { redirectTo: location.origin + location.pathname }
        });
        card.append(g);
      }
      const email = el('input', '', inputCss);
      email.type = 'email';
      email.placeholder = 'Your email';
      const m = el('button', 'Email me a login link', btnCss);
      m.onclick = async () => {
        if (!email.value) return;
        const { error } = await sb.auth.signInWithOtp({
          email: email.value,
          options: { emailRedirectTo: location.origin + location.pathname }
        });
        showLogin(error ? 'Could not send: ' + error.message : 'Check your email and tap the login link.');
      };
      const c = el('button', 'Close', linkCss);
      c.onclick = close;
      card.append(email, m, c);
    }

    function showForm(user) {
      card.replaceChildren();
      card.append(el('h3', 'Send us a message', 'margin:0'));
      card.append(el('p', 'Logged in as ' + user.email, 'margin:0;color:#555;font-size:14px'));
      const name = el('input', '', inputCss);
      name.placeholder = 'Your name';
      const msg = el('textarea', '', inputCss + ';height:110px');
      msg.placeholder = 'Your message (please do not write medical report details)';
      const send = el('button', 'Send', btnCss);
      const status = el('p', '', 'margin:0');
      send.onclick = async () => {
        if (!name.value.trim() || !msg.value.trim()) { status.textContent = 'Please fill both fields.'; return; }
        send.disabled = true;
        const { error } = await sb.from('inbox_messages').insert({ name: name.value.trim(), message: msg.value.trim() });
        send.disabled = false;
        if (error) { status.textContent = 'Could not send: ' + error.message; return; }
        name.value = '';
        msg.value = '';
        status.textContent = 'Message sent. We will reply soon.';
      };
      const out = el('button', 'Log out', linkCss);
      out.onclick = async () => { await sb.auth.signOut(); showLogin(); };
      const c = el('button', 'Close', linkCss);
      c.onclick = close;
      card.append(name, msg, send, status, out, c);
    }

    window.openInbox = async function () {
      overlay.style.display = 'flex';
      const { data } = await sb.auth.getSession();
      if (data.session) showForm(data.session.user); else showLogin();
    };

    const fab = el('button', 'Message us', 'position:fixed;left:12px;bottom:84px;z-index:9000;padding:12px 16px;border:0;border-radius:24px;background:#0a7;color:#fff;font-size:16px;box-shadow:0 2px 8px rgba(0,0,0,.3);cursor:pointer');
    fab.onclick = window.openInbox;
    document.body.appendChild(fab);
  }

  if (window.supabase) boot();
  else {
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
    s.onload = boot;
    document.head.appendChild(s);
  }
})();

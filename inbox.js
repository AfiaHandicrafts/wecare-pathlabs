(function () {
  const ENABLE_GOOGLE = true;
  const G = '<svg viewBox="0 0 48 48" width="22" height="22"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.5 5.4 2.6 13.2l7.9 6.1C12.4 13.6 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.7c-.6 3-2.2 5.5-4.7 7.2l7.6 5.9c4.4-4.1 6.9-10.1 6.9-17.6z"/><path fill="#FBBC05" d="M10.5 28.7c-.5-1.4-.8-3-.8-4.7s.3-3.2.8-4.7l-7.9-6.1C.9 16.5 0 20.1 0 24s.9 7.5 2.6 10.8l7.9-6.1z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.6-5.9c-2.1 1.4-4.9 2.3-8.3 2.3-6.3 0-11.6-4.1-13.5-9.8l-7.9 6.1C6.5 42.6 14.6 48 24 48z"/></svg>';

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

    const overlay = el('div', '', 'display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:99999;align-items:center;justify-content:center;padding:16px');
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

    const circle = el('button', '', 'position:absolute;top:62px;right:12px;z-index:9000;width:42px;height:42px;border-radius:50%;border:2px solid #fff;background:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.35);padding:0;overflow:hidden');
    circle.onclick = window.openInbox;
    document.body.appendChild(circle);

    async function updateCircle() {
      const { data } = await sb.auth.getSession();
      circle.replaceChildren();
      const u = data.session && data.session.user;
      if (!u) { circle.innerHTML = G; circle.title = 'Login'; return; }
      const av = u.user_metadata && (u.user_metadata.avatar_url || u.user_metadata.picture);
      if (av) {
        const im = el('img', '', 'width:100%;height:100%;object-fit:cover');
        im.referrerPolicy = 'no-referrer';
        im.src = av;
        circle.append(im);
      } else {
        circle.append(el('b', (u.email || '?')[0].toUpperCase(), 'font-size:18px;color:#0a7'));
      }
      circle.title = u.email;
    }
    sb.auth.onAuthStateChange(() => updateCircle());
    updateCircle();

    const fab = el('button', 'Message us', 'position:fixed;left:12px;bottom:100px;z-index:9000;padding:8px 14px;border:0;border-radius:20px;background:#0a7;color:#fff;font-size:14px;box-shadow:0 2px 8px rgba(0,0,0,.3);cursor:pointer');
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

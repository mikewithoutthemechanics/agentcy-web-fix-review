// Vercel Serverless Function — booking & contact form
// 1) Sends lead email to the team via Resend (instant, reliable)
// 2) Fires the n8n "PRD Creator" pipeline (client confirmation + PRD to team)
// Either side failing never blocks the other; the user always gets success.

const N8N_WEBHOOK = process.env.N8N_LEAD_WEBHOOK || 'https://n8n.agentcy.co.za/webhook/agentcy-lead';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();

  const { name, email, company, phone, engagement, message, pain, current_process, file_data } = req.body || {};
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required' });
  }
  const hasStory = (message && message !== '(via chat)') || pain || (file_data && file_data.length);
  if (!hasStory) {
    return res.status(400).json({ error: 'Tell us a little about what you need' });
  }

  const lead = {
    name: String(name).slice(0, 200),
    email: String(email).slice(0, 320),
    phone: String(phone || '').slice(0, 60),
    company: String(company || '').slice(0, 200),
    engagement: String(engagement || 'Not sure yet').slice(0, 120),
    message: String(message || '').slice(0, 4000),
    pain: String(pain || '').slice(0, 4000),
    current_process: String(current_process || '').slice(0, 4000),
  };

  // attachments: [{name, mime, data(base64)}] — max 3, 3MB each, forwarded to team email
  const ALLOWED = /\.(pdf|docx?|txt|md|csv|xlsx|png|jpe?g)$/i;
  const attachments = (Array.isArray(file_data) ? file_data : []).slice(0, 3).map(f => ({
    filename: String(f.name || 'attachment').slice(0, 120).replace(/[^\w.\- ()]/g, '_'),
    content: String(f.data || ''),
    content_type: String(f.mime || 'application/octet-stream').slice(0, 100),
  })).filter(a => a.content && ALLOWED.test(a.filename) && Buffer.byteLength(a.content, 'base64') <= 4_100_000);

  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  // --- 1) Direct team email (primary, must not fail silently) ---
  let emailOk = false;
  try {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      },
      body: JSON.stringify({
        from: 'Agentcy Bookings <bookings@concierge.agentcy.co.za>',
        to: (process.env.CONTACT_TO || 'ai@agentcy.co.za,michaelgraemek@gmail.com').split(',').map(s => s.trim()),
        reply_to: lead.email,
        subject: `New inquiry from ${lead.name}${lead.company && lead.company !== 'Not provided' ? ` (${lead.company})` : ''}`,
        html: `
          <h2>New ${lead.engagement === 'Request a call' ? 'Call Request' : 'Booking / Contact'} Submission</h2>
          <p><strong>Name:</strong> ${esc(lead.name)}</p>
          <p><strong>Email:</strong> ${esc(lead.email)}</p>
          ${lead.phone ? `<p><strong>Phone:</strong> ${esc(lead.phone)}</p>` : ''}
          ${lead.company ? `<p><strong>Company:</strong> ${esc(lead.company)}</p>` : ''}
          ${lead.engagement ? `<p><strong>Engagement:</strong> ${esc(lead.engagement)}</p>` : ''}
          ${lead.pain ? `<p><strong>Tired of dealing with:</strong></p><p>${esc(lead.pain).replace(/\n/g, '<br>')}</p>` : ''}
          ${lead.current_process ? `<p><strong>Current process:</strong></p><p>${esc(lead.current_process).replace(/\n/g, '<br>')}</p>` : ''}
          ${lead.message && lead.message !== '(via chat)' ? `<p><strong>Message:</strong></p><p>${esc(lead.message).replace(/\n/g, '<br>')}</p>` : ''}
          ${attachments.length ? `<p><strong>📎 Attachments:</strong> ${attachments.map(a => esc(a.filename)).join(', ')}</p>` : ''}
        `,
        ...(attachments.length ? { attachments } : {}),
      }),
    });
    emailOk = response.ok;
    if (!response.ok) {
      console.error('Resend error:', await response.text());
    }
  } catch (error) {
    console.error('Resend exception:', error);
  }

  // --- 2) Fire n8n PRD pipeline (best-effort; never blocks the response) ---
  let pipelineFired = false;
  try {
    const hook = await fetch(N8N_WEBHOOK, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(lead),
      signal: AbortSignal.timeout(8000),
    });
    pipelineFired = hook.ok;
    if (!hook.ok) {
      console.error('n8n webhook error:', hook.status, await hook.text().catch(() => ''));
    }
  } catch (error) {
    console.error('n8n webhook exception:', error);
  }

  return res.status(200).json({
    success: true,
    email: emailOk,
    pipeline: pipelineFired ? 'prd-creator-triggered' : 'skipped',
  });
}

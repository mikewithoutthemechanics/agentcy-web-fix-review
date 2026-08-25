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

  const { name, email, company, phone, engagement, message } = req.body || {};
  if (!name || !email || !message) {
    return res.status(400).json({ error: 'Name, email, and message are required' });
  }

  const lead = {
    name: String(name).slice(0, 200),
    email: String(email).slice(0, 320),
    phone: String(phone || '').slice(0, 60),
    company: String(company || '').slice(0, 200),
    engagement: String(engagement || 'Not sure yet').slice(0, 120),
    message: String(message).slice(0, 4000),
  };

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
          <h2>New Booking / Contact Submission</h2>
          <p><strong>Name:</strong> ${esc(lead.name)}</p>
          <p><strong>Email:</strong> ${esc(lead.email)}</p>
          ${lead.phone ? `<p><strong>Phone:</strong> ${esc(lead.phone)}</p>` : ''}
          ${lead.company ? `<p><strong>Company:</strong> ${esc(lead.company)}</p>` : ''}
          ${lead.engagement ? `<p><strong>Engagement:</strong> ${esc(lead.engagement)}</p>` : ''}
          <p><strong>Message:</strong></p>
          <p>${esc(lead.message).replace(/\n/g, '<br>')}</p>
        `,
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

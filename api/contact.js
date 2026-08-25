// Vercel Serverless Function - booking & contact via Resend
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  const { name, email, company, phone, engagement, message } = req.body || {};
  if (!name || !email || !message) {
    return res.status(400).json({ error: 'Name, email, and message are required' });
  }
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
        reply_to: email,
        subject: `New inquiry from ${name}${company ? ` (${company})` : ''}`,
        html: `
          <h2>New Booking / Contact Submission</h2>
          <p><strong>Name:</strong> ${name}</p>
          <p><strong>Email:</strong> ${email}</p>
          ${phone ? `<p><strong>Phone:</strong> ${phone}</p>` : ''}
          ${company ? `<p><strong>Company:</strong> ${company}</p>` : ''}
          ${engagement ? `<p><strong>Engagement:</strong> ${engagement}</p>` : ''}
          <p><strong>Message:</strong></p>
          <p>${String(message).replace(/\n/g, '<br>')}</p>
        `,
      }),
    });
    const data = await response.json();
    if (!response.ok) {
      return res.status(500).json({ error: 'Failed to send email', details: data });
    }
    return res.status(200).json({ success: true, id: data.id });
  } catch (error) {
    return res.status(500).json({ error: 'Server error' });
  }
}

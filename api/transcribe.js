// Vercel Serverless Function — voice note transcription via Groq Whisper
// Accepts multipart/form-data: audio=<file>. Returns { text }.

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const form = await req.formData();
    const file = form.get('audio');
    if (!file || typeof file === 'string') {
      return res.status(400).json({ error: 'Missing audio file' });
    }
    if (file.size > 4 * 1024 * 1024) {
      return res.status(413).json({ error: 'Voice note too large (max ~4MB / 90s)' });
    }

    const fd = new FormData();
    const ext = (file.name || 'voice.webm').split('.').pop();
    fd.append('file', file, 'voice-note.' + (ext || 'webm'));
    fd.append('model', 'whisper-large-v3-turbo');
    fd.append('response_format', 'json');

    const r = await fetch('https://api.groq.com/openai/v1/audio/transcriptions', {
      method: 'POST',
      headers: { Authorization: `Bearer ${process.env.GROQ_API_KEY}` },
      body: fd,
      signal: AbortSignal.timeout(25000),
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) {
      console.error('Groq transcription error:', r.status, j);
      return res.status(502).json({ error: 'Transcription failed' });
    }
    return res.status(200).json({ text: (j.text || '').trim() });
  } catch (err) {
    console.error('transcribe exception:', err);
    return res.status(500).json({ error: 'Server error' });
  }
}

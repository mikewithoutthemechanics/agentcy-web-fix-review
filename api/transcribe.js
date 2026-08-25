// Vercel Serverless Function — voice note transcription via Groq Whisper
// Accepts JSON: { audio_base64: string, mime?: string }. Returns { text }.
// (Vercel Node functions auto-parse JSON bodies; multipart is not available.)

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { audio_base64, mime } = req.body || {};
    if (!audio_base64) {
      return res.status(400).json({ error: 'Missing audio_base64' });
    }
    const buf = Buffer.from(audio_base64, 'base64');
    if (!buf || buf.length < 800) {
      return res.status(400).json({ error: 'Audio too short' });
    }
    if (buf.length > 4 * 1024 * 1024) {
      return res.status(413).json({ error: 'Voice note too large (max ~4MB)' });
    }

    const type = (mime || 'audio/webm').split(';')[0];
    const ext = type.includes('ogg') ? 'ogg' : type.includes('mp4') || type.includes('m4a') ? 'm4a' : type.includes('wav') ? 'wav' : type.includes('mpeg') ? 'mp3' : 'webm';

    const fd = new FormData();
    fd.append('file', new Blob([buf], { type }), 'voice-note.' + ext);
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
      console.error('Groq transcription error:', r.status, JSON.stringify(j).slice(0, 300));
      return res.status(502).json({ error: 'Transcription failed' });
    }
    return res.status(200).json({ text: (j.text || '').trim() });
  } catch (err) {
    console.error('transcribe exception:', err && err.message, err && err.stack);
    return res.status(500).json({ error: 'Server error' });
  }
}

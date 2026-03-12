const axios = require('axios');

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).send('Method Not Allowed');

  const { token } = req.body;
  const SECRET_KEY = process.env.TURNSTILE_SECRET_KEY

  try {
    const response = await axios.post(
      'https://challenges.cloudflare.com/turnstile/v0/siteverify',
      new URLSearchParams({
        secret: SECRET_KEY,
        response: token
      })
    );

    if (response.data.success) {
      res.setHeader('Set-Cookie', 'is_human=true; Path=/; Max-Age=3600; HttpOnly; SameSite=Strict');
      return res.status(200).json({ success: true });
    } else {
      return res.status(403).json({ success: false });
    }

  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}


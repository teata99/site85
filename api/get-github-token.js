export default async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Content-Type', 'application/json');

    if (req.method === 'OPTIONS') {
        return res.status(204).end();
    }

    const code = req.query.code || (req.body ? req.body.code : null);

    if (!code) {
        return res.status(400).json({ message: "code가 없습니다." });
    }

    const CLIENT_ID = process.env.GITHUB_CLIENT_ID;
    const CLIENT_SECRET = process.env.GITHUB_CLIENT_SECRET;

    try {
        const response = await fetch('https://github.com/login/oauth/access_token', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json', 
                'Accept': 'application/json' 
            },
            body: JSON.stringify({
                client_id: CLIENT_ID,
                client_secret: CLIENT_SECRET,
                code: code
            })
        });

        const data = await response.json();

        return res.status(200).json(data);

    } catch (error) {
        return res.status(500).json({ message: error.message });
    }
}
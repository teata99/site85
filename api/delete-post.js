export default async function handler(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS, PATCH');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(204).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Method Not Allowed' });
    }

    try {
        const { issueNumber } = req.body;
        const TOKEN = process.env.site85_token;

        if (!issueNumber) {
            return res.status(400).json({ message: "issueNumber가 필요합니다." });
        }

        const response = await fetch(`https://api.github.com/repos/teata99/site85/issues/${issueNumber}`, {
            method: 'PATCH',
            headers: {
                "Authorization": `token ${TOKEN}`,
                "Content-Type": "application/json",
                "Accept": "application/vnd.github.v3+json"
            },
            body: JSON.stringify({ state: 'closed' }) 
        });

        const data = await response.json();

        return res.status(response.status).json({ 
            message: "삭제(종료) 되었습니다.", 
            data 
        });

    } catch (error) {
        return res.status(500).json({ message: error.message });
    }
}
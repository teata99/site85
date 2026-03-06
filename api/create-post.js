export default async function handler(req, res) {
    
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');


    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Method Not Allowed' });
    }

    try {

        const { title, content } = req.body;
        const TOKEN = process.env.site85_token;

        const response = await fetch('https://api.github.com/repos/teata99/site85/issues', {
            method: 'POST',
            headers: {
                "Authorization": `token ${TOKEN}`,
                "Content-Type": "application/json",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Vercel-Serverless-Function"
            },
            body: JSON.stringify({ title, body: content })

        });

        const data = await response.json();

        return res.status(response.status).json(data);

    } catch (error) {
        console.error(error);
        return res.status(500).json({ message: 'Internal Server Error', error: error.message });
    }
    
}


            

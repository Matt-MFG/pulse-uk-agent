const http = require('http');
const https = require('https');
const url = require('url');

const TARGET_URL = 'https://pulse-agent-smcqmdg45a-uc.a.run.app';
const PORT = 3001;

const server = http.createServer((req, res) => {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Handle preflight requests
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    if (req.method === 'POST' && req.url === '/') {
        let body = '';

        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', () => {
            const parsedUrl = url.parse(TARGET_URL);

            const options = {
                hostname: parsedUrl.hostname,
                port: 443,
                path: '/',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(body)
                }
            };

            const proxyReq = https.request(options, (proxyRes) => {
                let responseData = '';

                proxyRes.on('data', (chunk) => {
                    responseData += chunk;
                });

                proxyRes.on('end', () => {
                    res.writeHead(proxyRes.statusCode, {'Content-Type': 'application/json'});
                    res.end(responseData);
                });
            });

            proxyReq.on('error', (error) => {
                console.error('Proxy error:', error);
                res.writeHead(500, {'Content-Type': 'application/json'});
                res.end(JSON.stringify({ error: 'Proxy error: ' + error.message }));
            });

            proxyReq.write(body);
            proxyReq.end();
        });
    } else {
        res.writeHead(404);
        res.end('Not found');
    }
});

server.listen(PORT, () => {
    console.log(`PULSE UK Agent proxy server running at http://localhost:${PORT}`);
    console.log(`Proxying requests to: ${TARGET_URL}`);
    console.log('\nOpen pulse_agent_interface.html in your browser and it will work through this proxy.');
});
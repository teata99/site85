export default async function handler(req, res) {
  const cookies = parseCookies(req.headers.cookie);

  if (cookies.is_human === 'true') {
    return res.status(200).send('<h1>🎉 인증 완료! 비밀 콘텐츠입니다.</h1>');
  } else {
    
    const cookiesToClear = ['is_human', 'cf_clearance']; 
    const clearCookieHeaders = cookiesToClear.map(name => 
      `${name}=; Path=/; Max-Age=0; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly; SameSite=Lax`
    );
    
    res.setHeader('Set-Cookie', clearCookieHeaders);

    return res.status(401).send('인증이 필요합니다.');
  }
}

function parseCookies(cookieHeader) {
  const cookies = {};
  cookieHeader?.split(';').forEach(cookie => {
    const [name, ...rest] = cookie.trim().split('=');
    cookies[name] = rest.join('=');
  });
  return cookies;
}

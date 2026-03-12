export default async function handler(req, res) {
  const cookies = req.headers.cookie || '';

  if (cookies.includes('is_human=true')) {
    return res.status(200).send('<h1>🎉 인증 완료! 비밀 콘텐츠입니다.</h1>');
  } else {
    return res.status(401).send('인증이 필요합니다.');
  }
}
const sharp = require('sharp');

const makeSvg = (content, w, h) => Buffer.from(`<svg width="${w}" height="${h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d0d1a"/>
      <stop offset="100%" stop-color="#12102a"/>
    </linearGradient>
    <linearGradient id="rainbow" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ff0000"/>
      <stop offset="20%" stop-color="#ff8800"/>
      <stop offset="40%" stop-color="#ffff00"/>
      <stop offset="60%" stop-color="#00cc00"/>
      <stop offset="80%" stop-color="#0088ff"/>
      <stop offset="100%" stop-color="#aa00ff"/>
    </linearGradient>
    <linearGradient id="card" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1e1b3a"/>
      <stop offset="100%" stop-color="#16142e"/>
    </linearGradient>
  </defs>
  <rect width="${w}" height="${h}" fill="url(#bg)"/>
  ${content}
</svg>`);

const featureSvg = makeSvg(`
  <rect y="468" width="1024" height="10" fill="url(#rainbow)" rx="2"/>
  <text x="512" y="180" font-family="Arial Black,Arial" font-weight="900" font-size="110" text-anchor="middle">
    <tspan fill="#ff6b9d">Gay</tspan><tspan fill="#ffffff"> App</tspan><tspan fill="#ffd700"> List</tspan>
  </text>
  <text x="512" y="270" font-family="Arial,sans-serif" font-size="34" text-anchor="middle" fill="#aaaacc">The world's only LGBTQ+ app directory</text>
  <text x="512" y="340" font-family="Arial,sans-serif" font-size="26" text-anchor="middle" fill="#666688">30+ apps · 5 regions · Global coverage</text>
  <text x="512" y="420" font-family="Arial,sans-serif" font-size="22" text-anchor="middle" fill="#ff6b9d">gay-app-list.vercel.app</text>
`, 1024, 500);

const ss1Svg = makeSvg(`
  <rect y="0" width="1080" height="6" fill="url(#rainbow)"/>
  <text x="540" y="120" font-family="Arial Black,Arial" font-weight="900" font-size="80" text-anchor="middle">
    <tspan fill="#ff6b9d">Gay</tspan><tspan fill="#ffffff"> App</tspan><tspan fill="#ffd700"> List</tspan>
  </text>
  <text x="540" y="175" font-family="Arial,sans-serif" font-size="26" text-anchor="middle" fill="#aaaacc">The world's only LGBTQ+ app directory</text>
  <text x="540" y="225" font-family="Arial,sans-serif" font-size="22" text-anchor="middle" fill="#666688">33 apps across 5 regions</text>
  <rect x="60" y="260" width="960" height="60" rx="30" fill="#1e1b3a" stroke="#333366" stroke-width="2"/>
  <text x="540" y="298" font-family="Arial,sans-serif" font-size="22" text-anchor="middle" fill="#555577">Search by name, country, audience...</text>
  <text x="80" y="380" font-family="Arial Black,Arial" font-weight="900" font-size="32" fill="#ff6b9d">Global Apps</text>
  <rect x="60" y="400" width="440" height="155" rx="16" fill="url(#card)" stroke="#2a2560" stroke-width="1"/>
  <text x="160" y="445" font-family="Arial Black,Arial" font-weight="700" font-size="26" fill="#ffffff">Grindr</text>
  <text x="160" y="475" font-family="Arial,sans-serif" font-size="20" fill="#888899">USA · Gay men · 2009</text>
  <text x="80" y="525" font-family="Arial,sans-serif" font-size="18" fill="#aaaacc">World's largest gay social network</text>
  <rect x="580" y="400" width="440" height="155" rx="16" fill="url(#card)" stroke="#2a2560" stroke-width="1"/>
  <text x="680" y="445" font-family="Arial Black,Arial" font-weight="700" font-size="26" fill="#ffffff">Scruff</text>
  <text x="680" y="475" font-family="Arial,sans-serif" font-size="20" fill="#888899">USA · Gay men · 2010</text>
  <text x="600" y="525" font-family="Arial,sans-serif" font-size="18" fill="#aaaacc">Community for bears and admirers</text>
  <rect x="60" y="575" width="440" height="155" rx="16" fill="url(#card)" stroke="#2a2560" stroke-width="1"/>
  <text x="160" y="620" font-family="Arial Black,Arial" font-weight="700" font-size="26" fill="#ffffff">HER</text>
  <text x="160" y="650" font-family="Arial,sans-serif" font-size="20" fill="#888899">USA · LGBTQ+ Women · 2013</text>
  <text x="80" y="700" font-family="Arial,sans-serif" font-size="18" fill="#aaaacc">Dating app for LGBTQ+ women</text>
  <rect x="580" y="575" width="440" height="155" rx="16" fill="url(#card)" stroke="#2a2560" stroke-width="1"/>
  <text x="680" y="620" font-family="Arial Black,Arial" font-weight="700" font-size="26" fill="#ffffff">Taimi</text>
  <text x="680" y="650" font-family="Arial,sans-serif" font-size="20" fill="#888899">USA · LGBTQ+ · 2017</text>
  <text x="600" y="700" font-family="Arial,sans-serif" font-size="18" fill="#aaaacc">All-inclusive LGBTQ+ social platform</text>
  <rect x="60" y="750" width="440" height="155" rx="16" fill="url(#card)" stroke="#2a2560" stroke-width="1"/>
  <text x="160" y="795" font-family="Arial Black,Arial" font-weight="700" font-size="26" fill="#ffffff">Hornet</text>
  <text x="160" y="825" font-family="Arial,sans-serif" font-size="20" fill="#888899">USA · Gay men · 2011</text>
  <text x="80" y="875" font-family="Arial,sans-serif" font-size="18" fill="#aaaacc">Gay social network with news</text>
  <rect x="580" y="750" width="440" height="155" rx="16" fill="url(#card)" stroke="#2a2560" stroke-width="1"/>
  <text x="680" y="795" font-family="Arial Black,Arial" font-weight="700" font-size="26" fill="#ffffff">Feeld</text>
  <text x="680" y="825" font-family="Arial,sans-serif" font-size="20" fill="#888899">UK · Open relationships · 2014</text>
  <text x="600" y="875" font-family="Arial,sans-serif" font-size="18" fill="#aaaacc">Dating for couples and singles</text>
  <rect y="1880" width="1080" height="6" fill="url(#rainbow)"/>
  <text x="540" y="1860" font-family="Arial,sans-serif" font-size="22" text-anchor="middle" fill="#666688">gay-app-list.vercel.app</text>
`, 1080, 1920);

const ss2Svg = makeSvg(`
  <rect y="0" width="1080" height="6" fill="url(#rainbow)"/>
  <text x="540" y="100" font-family="Arial Black,Arial" font-weight="900" font-size="60" text-anchor="middle">
    <tspan fill="#ff6b9d">Gay</tspan><tspan fill="#ffffff"> App</tspan><tspan fill="#ffd700"> List</tspan>
  </text>
  <text x="540" y="148" font-family="Arial,sans-serif" font-size="24" text-anchor="middle" fill="#aaaacc">Browse by Region</text>
  <text x="80" y="230" font-family="Arial Black,Arial" font-weight="900" font-size="32" fill="#ffd700">Asia &amp; Pacific</text>
  <rect x="60" y="248" width="440" height="148" rx="16" fill="url(#card)" stroke="#2a2560" stroke-width="1"/>
  <text x="160" y="295" font-family="Arial Black,Arial" font-weight="700" font-size="26" fill="#ffffff">Blued</text>
  <text x="160" y="325" font-family="Arial,sans-serif" font-size="20" fill="#888899">China · Gay men · 2012</text>
  <text x="80" y="372" font-family="Arial,sans-serif" font-size="18" fill="#aaaacc">Largest gay app in Asia, 58M users</text>
  <rect x="580" y="248" width="440" height="148" rx="16" fill="url(#card)" stroke="#2a2560" stroke-width="1"/>
  <text x="680" y="295" font-family="Arial Black,Arial" font-weight="700" font-size="26" fill="#ffffff">Fridae</text>
  <text x="680" y="325" font-family="Arial,sans-serif" font-size="20" fill="#888899">Singapore · LGBTQ+ · 2000</text>
  <text x="600" y="372" font-family="Arial,sans-serif" font-size="18" fill="#aaaacc">Pan-Asian LGBTQ+ network</text>
  <text x="80" y="450" font-family="Arial Black,Arial" font-weight="900" font-size="32" fill="#00ccff">Europe</text>
  <rect x="60" y="468" width="440" height="148" rx="16" fill="url(#card)" stroke="#2a2560" stroke-width="1"/>
  <text x="160" y="515" font-family="Arial Black,Arial" font-weight="700" font-size="26" fill="#ffffff">Romeo</text>
  <text x="160" y="545" font-family="Arial,sans-serif" font-size="20" fill="#888899">Germany · Gay men · 2002</text>
  <text x="80" y="592" font-family="Arial,sans-serif" font-size="18" fill="#aaaacc">Europe's leading gay social network</text>
  <rect x="580" y="468" width="440" height="148" rx="16" fill="url(#card)" stroke="#2a2560" stroke-width="1"/>
  <text x="680" y="515" font-family="Arial Black,Arial" font-weight="700" font-size="26" fill="#ffffff">Gaydar</text>
  <text x="680" y="545" font-family="Arial,sans-serif" font-size="20" fill="#888899">UK · Gay men · 1999</text>
  <text x="600" y="592" font-family="Arial,sans-serif" font-size="18" fill="#aaaacc">One of the original gay dating sites</text>
  <text x="80" y="670" font-family="Arial Black,Arial" font-weight="900" font-size="32" fill="#ff8800">Middle East</text>
  <rect x="60" y="688" width="440" height="148" rx="16" fill="url(#card)" stroke="#2a2560" stroke-width="1"/>
  <text x="160" y="735" font-family="Arial Black,Arial" font-weight="700" font-size="26" fill="#ffffff">Atraf</text>
  <text x="160" y="765" font-family="Arial,sans-serif" font-size="20" fill="#888899">Israel · LGBTQ+ · 2000</text>
  <text x="80" y="812" font-family="Arial,sans-serif" font-size="18" fill="#aaaacc">Leading LGBTQ+ app in Israel</text>
  <rect x="60" y="900" width="960" height="120" rx="20" fill="#1a1040" stroke="#ff6b9d" stroke-width="2"/>
  <text x="540" y="950" font-family="Arial Black,Arial" font-weight="900" font-size="28" text-anchor="middle" fill="#ff6b9d">The Complete LGBTQ+ App Directory</text>
  <text x="540" y="990" font-family="Arial,sans-serif" font-size="22" text-anchor="middle" fill="#aaaacc">30+ apps · Grindr to Blued · Global to Local</text>
  <text x="540" y="1020" font-family="Arial,sans-serif" font-size="20" text-anchor="middle" fill="#666688">Free · No signup required</text>
  <rect y="1880" width="1080" height="6" fill="url(#rainbow)"/>
  <text x="540" y="1860" font-family="Arial,sans-serif" font-size="22" text-anchor="middle" fill="#666688">gay-app-list.vercel.app</text>
`, 1080, 1920);

Promise.all([
  sharp(featureSvg).png().toFile('feature-graphic.png'),
  sharp(ss1Svg).png().toFile('screenshot1.png'),
  sharp(ss2Svg).png().toFile('screenshot2.png'),
]).then(() => console.log('Done!')).catch(e => console.error(e));

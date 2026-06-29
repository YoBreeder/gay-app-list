import sharp from 'sharp';
import { readFileSync } from 'fs';

const svg = readFileSync('./icon.svg');

await sharp(svg).resize(1024, 1024).png().toFile('./icon-1024.png');
console.log('✓ icon-1024.png (Apple App Store)');

await sharp(svg).resize(512, 512).png().toFile('./icon-512.png');
console.log('✓ icon-512.png (Google Play Store)');

await sharp(svg).resize(192, 192).png().toFile('./public/icon-192.png');
console.log('✓ icon-192.png (web/PWA)');

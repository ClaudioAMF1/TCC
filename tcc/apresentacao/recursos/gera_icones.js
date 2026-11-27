// Gera os ícones (Lucide, licença ISC) em PNG transparente, nas cores do deck.
const React = require('react');
const { renderToStaticMarkup } = require('react-dom/server');
const sharp = require('sharp');
const lu = require('react-icons/lu');
const path = require('path');
const NOMES = {
  celular: 'Smartphone', codigo: 'Code', sdk: 'Puzzle', servidor: 'Server', lei: 'Scale', busca: 'Search',
  escudo: 'ShieldCheck', escudo_alerta: 'ShieldAlert', usuarios: 'Users', documento: 'FileText', doc_busca: 'FileSearch',
  rede: 'Network', grafico: 'ChartBar', pizza: 'ChartPie', base: 'Database', download: 'Download', ok: 'CircleCheck',
  nao: 'CircleX', duvida: 'CircleHelp', proibido: 'Ban', globo: 'Earth', governo: 'Landmark', alvo: 'Target',
  ideia: 'Lightbulb', calendario: 'Calendar', alerta: 'TriangleAlert', livro: 'BookOpen', ciencia: 'FlaskConical',
  pacote: 'Package', camadas: 'Layers', olho: 'Eye', comparar: 'GitCompare', local: 'MapPin', scan: 'ScanSearch',
  martelo: 'Gavel', hash: 'Hash', lista: 'ListChecks', wifi: 'Wifi', impressao: 'Fingerprint', cadeado: 'Lock',
  monitor: 'MonitorSmartphone', microscopio: 'Microscope', prancheta: 'ClipboardList', filtro: 'Filter', rota: 'Route',
  fluxo: 'Workflow', biblioteca: 'Library', arquivo_ok: 'FileCheck', arquivo_x: 'FileX', relogio: 'Clock', enviar: 'Send',
  medidor: 'Gauge', sigma: 'Sigma', dividir: 'Split', pacotes: 'Boxes', info: 'Info', bandeira: 'Flag', atividade: 'Activity',
};
const CORES = { branco: '#FFFFFF', marinho: '#003D69', medio: '#7499BF' };
(async () => {
  for (const [nome, comp] of Object.entries(NOMES)) {
    for (const [cn, hex] of Object.entries(CORES)) {
      let svg = renderToStaticMarkup(React.createElement(lu['Lu' + comp], { size: 512, strokeWidth: 1.75 }));
      svg = svg.replace(/currentColor/g, hex);
      if (!svg.includes('xmlns=')) svg = svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
      await sharp(Buffer.from(svg)).png().toFile(path.join(process.argv[2] || path.join(__dirname, 'icones'), `${nome}_${cn}.png`));
    }
  }
  console.log('ícones:', Object.keys(NOMES).length, 'x', Object.keys(CORES).length);
})();

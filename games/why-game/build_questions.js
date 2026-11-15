// 由 parts/*.txt 產生 questions.js。執行：node build_questions.js
// 每行格式（用 | 分隔，共 8 欄）：
//   層級|分類|問題|正確答案|錯誤1|錯誤2|錯誤3|有趣解釋
// 層級：k＝孩子題、a＝大人題
const fs = require('fs');
const CATS = {
  kitchen: '廚房吃喝', body: '身體小祕密', sky: '天空天氣', home: '居家日用',
  nature: '動物植物', go: '出門交通', tech: '科技電器', odd: '生活怪事'
};
const LEVELS = new Set(['k', 'a']);
const hash = s => { let h = 5381; for (const ch of s) h = ((h * 33) ^ ch.codePointAt(0)) >>> 0; return h.toString(36); };
const errors = [], warns = [];
const cards = [], seenQ = new Map();
const files = fs.readdirSync('parts').filter(f => f.endsWith('.txt')).sort();
const hasCJK = s => /[一-鿿]/.test(s);
for (const f of files) {
  fs.readFileSync(`parts/${f}`, 'utf8').split('\n').forEach((line, i) => {
    if (!line.trim() || line.startsWith('#')) return;
    const where = `${f}:${i + 1}`;
    const p = line.split('|').map(x => x.trim());
    if (p.length !== 8) return errors.push(`${where} 欄位數=${p.length}（應為 8）：${line.slice(0, 40)}`);
    const [lv, cat, q, ans, w1, w2, w3, why] = p;
    if (!LEVELS.has(lv)) errors.push(`${where} 層級錯誤 ${lv}`);
    if (!CATS[cat]) errors.push(`${where} 分類錯誤 ${cat}`);
    if (!q.endsWith('？')) errors.push(`${where} 問題要以全形問號結尾：${q}`);
    if (q.length > 40) errors.push(`${where} 問題太長(${q.length})：${q}`);
    const opts = [ans, w1, w2, w3];
    opts.forEach(o => { if (!o) errors.push(`${where} 有空白選項`); else if (o.length > 24) errors.push(`${where} 選項太長(${o.length})：${o}`); });
    if (new Set(opts).size !== 4) errors.push(`${where} 選項有重複：${q}`);
    if (!why || why.length > 90) errors.push(`${where} 解釋缺少或太長(${why.length})：${q}`);
    [q, ...opts, why].forEach(t => { if (/[ㄅ-ㄩ]/.test(t)) errors.push(`${where} 含注音符號`); });
    if (!hasCJK(q)) errors.push(`${where} 問題沒有中文`);
    if (seenQ.has(q)) errors.push(`${where} 問題重複（與 ${seenQ.get(q)} 相同）：${q}`);
    seenQ.set(q, where);
    // 正確答案太常是最長選項，玩家會學會「選最長的」
    cards.push({ id: 'w' + hash(q), level: lv, cat, q, opts, why, longest: ans.length > Math.max(w1.length, w2.length, w3.length), shortest: ans.length < Math.min(w1.length, w2.length, w3.length) });
  });
}
const count = (arr, f) => arr.reduce((m, c) => (m[f(c)] = (m[f(c)] || 0) + 1, m), {});
console.log('題數', cards.length);
console.log('層級', count(cards, c => c.level));
console.log('分類', count(cards, c => c.cat));
const longestRate = cards.filter(c => c.longest).length / (cards.length || 1);
const shortestRate = cards.filter(c => c.shortest).length / (cards.length || 1);
console.log('正確答案是最長選項的比例', (longestRate * 100).toFixed(0) + '%；是最短選項的比例', (shortestRate * 100).toFixed(0) + '%（理想約 25%，12%～40% 以內才算均衡）');
if (longestRate > 0.4 || longestRate < 0.12) warns.push('正確答案「最長」比例不均衡');
if (shortestRate > 0.4 || shortestRate < 0.12) warns.push('正確答案「最短」比例不均衡');
const ids = new Set(cards.map(c => c.id)); if (ids.size !== cards.length) errors.push('id 衝突');
if (warns.length) console.log('提醒\n' + warns.join('\n'));
if (errors.length) { console.log('錯誤 ' + errors.length + ' 個\n' + errors.join('\n')); process.exit(1); }
console.log('錯誤 0 個');
const out = cards.map(({ longest, shortest, ...c }) => c);
fs.writeFileSync('questions.js', '// 自動產生，請改 parts/*.txt，不要手改。\nwindow.WG_DATA = ' + JSON.stringify({ cats: CATS, cards: out }) + ';\n');
console.log('已寫入 questions.js', fs.statSync('questions.js').size, 'bytes');

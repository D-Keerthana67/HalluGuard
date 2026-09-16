from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import json, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT=Path(__file__).resolve().parents[1]
app=Flask(__name__, static_folder=str(ROOT/'frontend'))
CORS(app)
KB=json.loads((ROOT/'data'/'knowledge_base.json').read_text(encoding='utf-8'))
texts=[x['text'] for x in KB]
vec=TfidfVectorizer(stop_words='english'); matrix=vec.fit_transform(texts)

def claims(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if len(s.strip())>=8]

def evidence(claim):
    q=vec.transform([claim]); scores=cosine_similarity(q,matrix)[0]
    ids=sorted(range(len(scores)), key=lambda i:scores[i], reverse=True)[:3]
    return [{'text':KB[i]['text'],'source':KB[i]['source'],'score':round(float(scores[i]),3)} for i in ids]

def verify(claim, ev):
    best=ev[0]['score'] if ev else 0
    neg_claim=bool(re.search(r'\b(not|no|never|false|isn\'t|aren\'t|wasn\'t|weren\'t)\b',claim.lower()))
    neg_ev=bool(re.search(r'\b(not|no|never|false|isn\'t|aren\'t|wasn\'t|weren\'t)\b',ev[0]['text'].lower())) if ev else False
    if best<0.10: return 'UNSUPPORTED',best
    if neg_claim != neg_ev and best>=0.18: return 'CONTRADICTED',best
    if best>=0.42: return 'SUPPORTED',best
    return 'PARTIALLY_SUPPORTED',best

def classify(claim, verdict):
    low=claim.lower()
    if any(w in low for w in ['2020','2021','2022','2023','2024','2025','2026','today','yesterday']): typ='TEMPORAL'
    elif any(c.isdigit() for c in claim): typ='NUMERICAL'
    elif 'citation' in low or 'source' in low or 'according to' in low: typ='CITATION'
    else: typ='FACTUAL'
    severity='LOW' if verdict=='SUPPORTED' else ('MEDIUM' if verdict=='PARTIALLY_SUPPORTED' else 'HIGH')
    return typ,severity

def analyze(text):
    rows=[]
    for c in claims(text):
        ev=evidence(c); v,score=verify(c,ev); typ,sev=classify(c,v)
        correction=c if v=='SUPPORTED' else (ev[0]['text'] if ev else 'UNVERIFIED')
        rv,_=verify(correction,evidence(correction)) if correction!='UNVERIFIED' else ('UNSUPPORTED',0)
        rows.append({'claim':c,'verdict':v,'score':round(score,3),'type':typ,'severity':sev,'evidence':ev,'correction':correction,'reverification':rv})
    n=len(rows); supported=sum(r['verdict']=='SUPPORTED' for r in rows); partial=sum(r['verdict']=='PARTIALLY_SUPPORTED' for r in rows)
    reliability=round(((supported+0.5*partial)/n)*100,1) if n else 0
    label='HIGH' if reliability>=80 else ('MEDIUM' if reliability>=50 else 'LOW')
    return {'input':text,'claims':rows,'reliability_score':reliability,'reliability_label':label,'claim_count':n}

@app.get('/api/health')
def health(): return jsonify({'status':'ok','service':'HalluGuard'})
@app.post('/api/analyze')
def api_analyze():
    data=request.get_json(silent=True) or {}; text=str(data.get('text','')).strip()
    if not text: return jsonify({'error':'text is required'}),400
    return jsonify(analyze(text))
@app.get('/')
def home(): return send_from_directory(ROOT/'frontend','index.html')
@app.get('/<path:path>')
def static(path): return send_from_directory(ROOT/'frontend',path)

if __name__=='__main__': app.run(host='127.0.0.1',port=5000,debug=True)

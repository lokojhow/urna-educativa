from pathlib import Path

p=Path('offline-app.js')
s=p.read_text()
s=s.replace("currentInterview=null,db=null,photoUrls=new Map();","currentInterview=null,db=null,photoUrls=new Map(),voteHistory=[];")
s=s.replace("function office(){return cargos[step]||null}function candidate(){const o=office();return o?cands.find(c=>c.cargo_id===o.id&&String(c.numero)===typed)||null:null}","function office(){return cargos[step]||null}function candidate(){const o=office();return o?cands.find(c=>String(c.cargo_id)===String(o.id)&&String(c.numero)===typed)||null:null}function repeatedSenator(c,o){if(!c||!o||!/Senador/i.test(o.nome)||!/2/.test(o.nome))return false;const first=voteHistory.find(a=>/Senador/i.test(a.cargo_nome)&&a.tipo_resposta==='candidato');return !!first&&String(first.numero_digitado)===String(typed)}")
s=s.replace("function beginVote(m){mode=m;step=0;typed='';blank=false;currentInterview=null;","function beginVote(m){mode=m;step=0;typed='';blank=false;currentInterview=null;voteHistory=[];")
s=s.replace("step=0;typed='';blank=false;mode='pesquisa';$('voteModeLabel')","step=0;typed='';blank=false;voteHistory=[];mode='pesquisa';$('voteModeLabel')")
start=s.index('async function render(){')
end=s.index('\nasync function startResearch',start)
new_render='''async function render(){const o=office();if(!o){$('screen').innerHTML=`<div class="finish"><b>FIM</b><span>${mode==='treino'?'Treinamento concluído — nada foi gravado.':'Pesquisa salva no celular. '+(navigator.onLine?'Sincronizando…':'Será sincronizada quando houver internet.')}</span><button class="primary" onclick="novaEntrevista()">NOVA PESQUISA</button></div>`;finishSound();if(mode==='pesquisa'&&currentInterview){currentInterview.status='concluida';currentInterview.finishedAt=new Date().toISOString();await put('interviews',currentInterview);refreshOfflineInfo();if(net())syncPending()}return}$('office').textContent=o.nome;$('digits').innerHTML=Array.from({length:o.digitos},(_,i)=>`<div class="digit">${typed[i]||''}</div>`).join('');let c=candidate();const dup=repeatedSenator(c,o),full=typed.length===Number(o.digitos),isNull=!blank&&full&&(!c||dup);$('blankLabel').textContent=blank?'VOTO EM BRANCO':'VOTO NULO';$('blankLabel').classList.toggle('show',blank||isNull);$('cand').classList.toggle('show',!!c&&!blank&&!dup);if(c&&!dup){$('cname').textContent=c.nome;$('cparty').textContent=(c.partido||'')+' • '+c.numero;$('cphoto').src=await photoBlob(c)}}
function restoreVoteScreen(){$('screen').innerHTML='<small id="voteModeLabel">SEU VOTO PARA</small><div class="office" id="office"></div><div>Digite o número do candidato.</div><div class="digits" id="digits"></div><div class="cand" id="cand"><div><h2 id="cname"></h2><b id="cparty"></b></div><img id="cphoto"></div><div class="blank" id="blankLabel">VOTO EM BRANCO</div>'}
function novaEntrevista(){restoreVoteScreen();step=0;typed='';blank=false;voteHistory=[];currentInterview=null;if(mode==='treino'){show('modeView');return}['name','phone','city','district','address'].forEach(id=>{if($(id))$(id).value=''});if($('age'))$('age').value='';if($('sex'))$('sex').value='';if($('consent'))$('consent').checked=false;$('startErr').textContent='';show('startView')}
'''
s=s[:start]+new_render+s[end:]
start=s.index('async function confirmVote(){')
end=s.index('\nasync function syncOne',start)
new_confirm='''async function confirmVote(){const o=office();if(!o)return;if(!blank&&typed.length!==Number(o.digitos))return;let c=candidate(),tipo='nulo';const dup=repeatedSenator(c,o);if(blank)tipo='branco';else if(c&&!dup)tipo='candidato';else{tipo='nulo';c=null}const answer={cargo_id:o.id,cargo_nome:o.nome,candidato_id:c?.id||null,numero_digitado:typed||null,tipo_resposta:tipo,ordem:step+1};voteHistory.push(answer);if(mode==='pesquisa'&&currentInterview){currentInterview.answers.push({cargo_id:answer.cargo_id,candidato_id:answer.candidato_id,numero_digitado:answer.numero_digitado,tipo_resposta:answer.tipo_resposta,ordem:answer.ordem});await put('interviews',currentInterview)}confirmSound();step++;typed='';blank=false;render()}
'''
s=s[:start]+new_confirm+s[end:]
p.write_text(s)

p=Path('admin-v4.html')
s=p.read_text()
start=s.index('function renderTop3(){')
end=s.index('function participantLabel',start)
new_top='''function renderTop3(){const agg=results.agregados||{},names=Object.keys(agg);$('top3').innerHTML=names.length?names.map(cargo=>{const data=agg[cargo]||{},top=Object.entries(data).filter(([n])=>n!=='NULO'&&n!=='BRANCO').sort((a,b)=>b[1]-a[1]).slice(0,3),nulo=Number(data.NULO||0),branco=Number(data.BRANCO||0),all=[...top.map(([n,v],i)=>({label:(i+1)+'º '+n,value:Number(v)})),{label:'VOTOS NULOS',value:nulo},{label:'VOTOS EM BRANCO',value:branco}],max=Math.max(1,...all.map(x=>x.value));return `<div class="rankcard"><h3>${esc(cargo)}</h3>${all.map(x=>`<div class="rankrow"><div class="rankhead"><span>${esc(x.label)}</span><span>${x.value}</span></div><div class="bar"><div class="fill" style="width:${x.value/max*100}%"></div></div></div>`).join('')}</div>`}).join(''):'<div class="card">Ainda não há resultados para exibir.</div>'}'''
s=s[:start]+new_top+s[end:]
p.write_text(s)

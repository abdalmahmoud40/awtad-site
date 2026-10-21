(function(){
  var EN=document.documentElement.lang==='en';
  // تصفية حسب القسم
  var chips=document.querySelectorAll('.jchips button');
  chips.forEach(function(c){c.addEventListener('click',function(){
    var d=c.getAttribute('data-d');
    chips.forEach(function(x){x.setAttribute('aria-pressed',x===c);});
    document.querySelectorAll('.job').forEach(function(j){j.hidden=!!d&&j.getAttribute('data-d')!==d;});
  });});
  // نسخ رابط الوظيفة
  document.querySelectorAll('.copy-link').forEach(function(b){b.addEventListener('click',function(){
    var u=b.getAttribute('data-url'),t=b.textContent;
    var done=function(){b.textContent=b.getAttribute('data-done');setTimeout(function(){b.textContent=t;},2000);};
    if(navigator.clipboard){navigator.clipboard.writeText(u).then(done,function(){prompt('',u);});}else{prompt('',u);}
  });});
  // نموذج التقديم
  var f=document.getElementById('applyForm'); if(!f) return;
  var inp=document.getElementById('acv'),nm=document.getElementById('acvName'),drop=f.querySelector('.drop');
  var err=document.getElementById('applyErr'),btn=document.getElementById('applyBtn'),ok=document.getElementById('applyOk');
  var MAX=5*1024*1024, okExt=/\.(pdf|docx?|DOCX?|PDF)$/;
  var msg={fields:EN?'Please fill in all required fields and accept the consent box.':'أكمل كل الحقول المطلوبة ووافق على حفظ البيانات.',
    email:EN?'Please enter a valid email address.':'اكتب بريداً إلكترونياً صحيحاً.',
    cv:EN?'Please attach your CV.':'أرفق سيرتك الذاتية.',
    size:EN?'The CV must be under 5 MB.':'حجم السيرة الذاتية يجب أن يكون أقل من 5 ميغابايت.',
    type:EN?'The CV must be a PDF or Word file.':'السيرة الذاتية يجب أن تكون بصيغة PDF أو Word.',
    closed:EN?'This position is no longer accepting applications.':'انتهى التقديم على هذه الوظيفة.',
    rate:EN?'Too many applications from this connection. Please try again later.':'أُرسلت طلبات كثيرة من هذا الاتصال. حاول مرة أخرى لاحقاً.',
    net:EN?'Connection problem. Check your internet and try again.':'تعذر الاتصال. تأكد من الإنترنت ثم أعد المحاولة.'};
  function show(){var x=inp.files&&inp.files[0];nm.textContent=x?x.name+' ('+(x.size/1048576).toFixed(1)+' MB)':'';}
  inp.addEventListener('change',show);
  ['dragenter','dragover'].forEach(function(e){drop.addEventListener(e,function(ev){ev.preventDefault();drop.classList.add('over');});});
  ['dragleave','drop'].forEach(function(e){drop.addEventListener(e,function(ev){ev.preventDefault();drop.classList.remove('over');});});
  drop.addEventListener('drop',function(ev){if(ev.dataTransfer.files.length){inp.files=ev.dataTransfer.files;show();}});
  f.addEventListener('submit',function(e){
    e.preventDefault(); err.textContent='';
    var req=['an','ae','ap','ac','ax'];
    for(var i=0;i<req.length;i++){if(!document.getElementById(req[i]).value.trim()){err.textContent=msg.fields;document.getElementById(req[i]).focus();return;}}
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(document.getElementById('ae').value.trim())){err.textContent=msg.email;return;}
    var x=inp.files&&inp.files[0];
    if(!x){err.textContent=msg.cv;return;} if(x.size>MAX){err.textContent=msg.size;return;} if(!okExt.test(x.name)){err.textContent=msg.type;return;}
    if(!f.querySelector('[name=consent]').checked){err.textContent=msg.fields;return;}
    btn.disabled=true; var label=btn.textContent; btn.textContent=EN?'Sending…':'جارٍ الإرسال…';
    fetch('/api/apply',{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}})
      .then(function(r){return r.json().catch(function(){return {ok:false,error:'net'};});})
      .then(function(d){
        if(d.ok){Array.prototype.forEach.call(f.children,function(c){if(c!==ok&&c.tagName!=='H2')c.hidden=true;});ok.hidden=false;ok.scrollIntoView({behavior:'smooth',block:'center'});}
        else{err.textContent=msg[d.error]||msg.fields;btn.disabled=false;btn.textContent=label;}
      },function(){err.textContent=msg.net;btn.disabled=false;btn.textContent=label;});
  });
})();

(function(){
  var EN=document.documentElement.lang==='en', WA='https://wa.me/249912340786?text=';
  var b=document.querySelector('.menu-btn'),n=document.getElementById('nav');
  if(b&&n){b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o);});}
  var y=document.getElementById('yr'); if(y) y.textContent=new Date().getFullYear();
  var g=function(id){var e=document.getElementById(id);return e?e.value.trim():'';};
  document.querySelectorAll('.chips button').forEach(function(c){c.addEventListener('click',function(){
    var f=c.getAttribute('data-f');
    document.querySelectorAll('.chips button').forEach(function(x){x.setAttribute('aria-pressed',x===c);});
    document.querySelectorAll('.prod').forEach(function(p){p.hidden=!(f==='all'||p.getAttribute('data-cat')===f);});
  });});
  function bind(id,req,errId,build){var f=document.getElementById(id); if(!f) return;
    f.addEventListener('submit',function(e){e.preventDefault();
      var err=document.getElementById(errId);
      for(var i=0;i<req.length;i++){if(!g(req[i])){err.textContent=EN?'Please fill in the required fields.':'أكمل الحقول المطلوبة ثم أعد الإرسال.';return;}}
      err.textContent=''; window.open(WA+encodeURIComponent(build()),'_blank','noopener');});}
  bind('quoteForm',['qn','qp'],'quoteErr',function(){return EN?
    ('Quote request - Awtad website\nName: '+g('qn')+'\nPhone: '+g('qp')+'\nSector: '+g('qs')+(g('qq')?'\nQuantity: '+g('qq'):'')+(g('qm')?'\n\n'+g('qm'):'')):
    ('طلب عرض سعر - موقع أوتاد\nالاسم: '+g('qn')+'\nالهاتف: '+g('qp')+'\nالقطاع: '+g('qs')+(g('qq')?'\nالكمية: '+g('qq'):'')+(g('qm')?'\n\n'+g('qm'):''));});
  bind('partnerForm',['pc','pn','pp'],'partnerErr',function(){return EN?
    ('Partnership request - Awtad website\nCompany: '+g('pc')+'\nContact: '+g('pn')+'\nPhone: '+g('pp')+'\nType: '+g('pt')+(g('pm')?'\n\n'+g('pm'):'')):
    ('طلب شراكة - موقع أوتاد\nالشركة: '+g('pc')+'\nالمسؤول: '+g('pn')+'\nالهاتف: '+g('pp')+'\nنوع الشراكة: '+g('pt')+(g('pm')?'\n\n'+g('pm'):''));});
})();

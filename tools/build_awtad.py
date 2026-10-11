import json, os, re, urllib.parse
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public') + os.sep
DOMAIN = 'https://awtad-trade.com'
PHONE = '249912340786'; PHONE_TXT = '+249 91 234 0786'
EMAIL = 'info@awtad-trade.com'
WA = f'https://wa.me/{PHONE}'
MAP_Q = 'Wad Madani, Sudan'
MAP_EMBED = 'https://www.google.com/maps?q=' + urllib.parse.quote_plus(MAP_Q) + '&output=embed'
MAP_LINK = 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote_plus(MAP_Q)

def svg(p, extra=''):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}>{p}</svg>'
I = {
 'phone': svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>'),
 'badge': svg('<circle cx="12" cy="8" r="6"/><path d="M15.5 13 17 22l-5-3-5 3 1.5-9"/>'),
 'users': svg('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>'),
 'truck': svg('<path d="M1 3h15v13H1zM16 8h4l3 3v5h-7"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>'),
 'shield': svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>'),
 'leaf': svg('<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>'),
 'chat': svg('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'),
 'flask': svg('<path d="M9 3h6M10 3v6L4 19a2 2 0 0 0 1.7 3h12.6A2 2 0 0 0 20 19l-6-10V3"/><path d="M7 15h10"/>'),
 'list': svg('<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>'),
 'refresh': svg('<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>'),
 'menu': svg('<path d="M4 6h16M4 12h16M4 18h16"/>', ' width="24" height="24"'),
 'globe': svg('<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/>'),
}
WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>'
SLAB = '<span class="slab" aria-hidden="true"><i></i><i></i></span>'

# ---------------- القطاعات ----------------
SECT = [
 dict(id='feed', img='p-pellets',
  ar=('قطاع الأعلاف','أعلاف متكاملة للدواجن والماشية والتسمين بأعلى معايير الجودة.',
      'نوفر أعلافاً متكاملة لمراحل التربية المختلفة: علف بادئ ونامي وناهي للدواجن، وأعلاف تسمين للماشية، بتركيبات متوازنة تدعم النمو وكفاءة التحويل الغذائي.',
      ['أعلاف الدواجن (بادئ، نامي، ناهي)','أعلاف تسمين الماشية','تركيبات متوازنة حسب مرحلة التربية','توريد للمزارع والموزعين']),
  en=('Animal Feed','Complete feeds for poultry, cattle and fattening, made to high quality standards.',
      'We supply complete feeds for every rearing stage: starter, grower and finisher feeds for poultry, plus cattle fattening feed, with balanced formulas that support growth and feed conversion.',
      ['Poultry feed (starter, grower, finisher)','Cattle fattening feed','Balanced formulas for each rearing stage','Supply to farms and distributors'])),
 dict(id='feed-inputs', img='p-lysine',
  ar=('مدخلات صناعة الأعلاف','مواد خام ومركزات عالية الجودة لصناعة الأعلاف.',
      'نستورد ونوفر لمصانع الأعلاف ومزارع الإنتاج المواد الخام والإضافات الأساسية: الأحماض الأمينية مثل اللايسين، والمركزات البروتينية، وخلطات الفيتامينات والمعادن (البريمكس).',
      ['الأحماض الأمينية (لايسين)','المركزات البروتينية','بريمكس الفيتامينات والمعادن','توريد بالجملة لمصانع الأعلاف']),
  en=('Feed Manufacturing Inputs','High-quality raw materials and concentrates for feed manufacturing.',
      'We import and supply feed mills and production farms with essential raw materials and additives: amino acids such as lysine, protein concentrates and vitamin-mineral premixes.',
      ['Amino acids (lysine)','Protein concentrates','Vitamin and mineral premix','Bulk supply to feed mills'])),
 dict(id='veterinary', img='p-antibiotic',
  ar=('الأدوية البيطرية','أدوية ولقاحات بيطرية لصحة الحيوان.',
      'نوفر أدوية بيطرية للدواجن والماشية تشمل المضادات الحيوية واسعة الطيف ومحاليل الفيتامينات، مع إرشاد فني حول الاستخدام الصحيح والجرعات بالتنسيق مع الطبيب البيطري.',
      ['مضادات حيوية بيطرية','محاليل فيتامينات','مستلزمات صحة الحيوان','إرشاد فني للمربين']),
  en=('Veterinary Medicines','Veterinary medicines and vaccines for animal health.',
      'We supply veterinary medicines for poultry and cattle, including broad-spectrum antibiotics and vitamin solutions, with technical guidance on correct use and dosing in coordination with a veterinarian.',
      ['Veterinary antibiotics','Vitamin solutions','Animal health supplies','Technical guidance for breeders'])),
 dict(id='agrochemicals', img='sprayer',
  ar=('الأدوية الزراعية','مبيدات وأسمدة زراعية لحماية المحاصيل.',
      'نوفر للمزارعين مبيدات حشرية واسعة المدى وأسمدة مركبة متوازنة لتحسين إنتاجية المحاصيل وحمايتها، مع توجيه حول الاستخدام الآمن.',
      ['مبيدات حشرية زراعية','أسمدة مركبة وعضوية','حماية المحاصيل','إرشاد حول الاستخدام الآمن']),
  en=('Agrochemicals','Pesticides and fertilizers to protect crops.',
      'We supply farmers with broad-spectrum insecticides and balanced compound fertilizers to protect crops and raise yields, with guidance on safe use.',
      ['Agricultural insecticides','Compound and organic fertilizers','Crop protection','Guidance on safe use'])),
 dict(id='livestock', img='cattle',
  ar=('الإنتاج الحيواني','مشاريع تربية وبرامج تسمين متكاملة.',
      'ندعم مشاريع تربية الدواجن وتسمين الماشية من خلال توفير المدخلات اللازمة من أعلاف وأدوية، وبرامج تغذية ورعاية تساعد على رفع الإنتاجية.',
      ['دعم مشاريع الدواجن','برامج تسمين الماشية','برامج تغذية ورعاية','توريد المدخلات للمشاريع']),
  en=('Livestock Production','Integrated rearing projects and fattening programmes.',
      'We support poultry and cattle fattening projects by supplying the feeds and medicines they need, with feeding and care programmes that help raise productivity.',
      ['Poultry project support','Cattle fattening programmes','Feeding and care programmes','Inputs supply for projects'])),
 dict(id='agriculture', img='field',
  ar=('الإنتاج الزراعي','دعم شامل للمشاريع الزراعية.',
      'نقف مع المزارعين في مراحل الموسم الزراعي بتوفير الأسمدة ومستلزمات حماية المحاصيل والمدخلات الزراعية، ونرشدهم لاختيار ما يناسب أرضهم ومحصولهم.',
      ['المدخلات الزراعية','الأسمدة ومستلزمات الحماية','دعم المزارعين خلال الموسم','إرشاد حسب المحصول']),
  en=('Agricultural Production','Comprehensive support for farming projects.',
      'We stand with farmers through the season by supplying fertilizers, crop protection supplies and agricultural inputs, and advise them on what suits their land and crop.',
      ['Agricultural inputs','Fertilizers and crop protection','Support through the season','Crop-specific advice'])),
]

# ---------------- المنتجات ----------------
CATS = {'poultry':('أعلاف الدواجن','Poultry feed'),'cattle':('أعلاف الماشية','Cattle feed'),'inputs':('مدخلات الأعلاف','Feed inputs'),
        'vet':('أدوية بيطرية','Veterinary'),'agro':('أدوية زراعية','Agrochemicals')}
PROD = [
 ('inputs','p-lysine',('الأحماض الأمينية - لايسين','بودرة اللايسين حمض أميني أساسي يُستخدم على نطاق واسع في صناعة الأعلاف لتحسين قيمتها الغذائية ودعم النمو الصحي، ويساعد على تحقيق التوازن الأميني وزيادة كفاءة الاستفادة من البروتين.'),
                     ('Amino Acids - Lysine','Lysine powder is an essential amino acid widely used in feed manufacturing to raise nutritional value and support healthy growth. It helps balance amino acids and improves protein utilisation.')),
 ('poultry','p-starter',('علف بادئ للدواجن','علف بادئ متكامل للكتاكيت من عمر يوم حتى 21 يوماً.'),('Poultry Starter Feed','Complete starter feed for chicks from day 1 to day 21.')),
 ('poultry','p-starter',('علف نامي للدواجن','علف نامي للدجاج من عمر 22 يوماً حتى 35 يوماً.'),('Poultry Grower Feed','Grower feed for chickens from day 22 to day 35.')),
 ('poultry','p-pellets',('علف ناهي للدواجن','علف ناهي للتسمين من عمر 36 يوماً حتى التسويق.'),('Poultry Finisher Feed','Finisher feed from day 36 until marketing.')),
 ('cattle','p-pellets',('علف ماشية للتسمين','علف متكامل لتسمين الماشية.'),('Cattle Fattening Feed','Complete feed for fattening cattle.')),
 ('inputs','p-protein',('مركزات بروتينية','مركزات بروتينية عالية الجودة لصناعة الأعلاف.'),('Protein Concentrates','High-quality protein concentrates for feed manufacturing.')),
 ('inputs','p-premix',('بريمكس فيتامينات ومعادن','خليط فيتامينات ومعادن للأعلاف.'),('Vitamin & Mineral Premix','A vitamin and mineral blend for feeds.')),
 ('vet','p-antibiotic',('مضادات حيوية واسعة الطيف','مضادات حيوية بيطرية واسعة المدى.'),('Broad-Spectrum Antibiotics','Broad-spectrum veterinary antibiotics.')),
 ('vet','p-vitamins',('فيتامينات','محاليل فيتامينات للحيوانات.'),('Vitamins','Vitamin solutions for animals.')),
 ('agro','p-insecticide',('مبيدات حشرية زراعية','مبيدات حشرية واسعة المدى للمحاصيل.'),('Agricultural Insecticides','Broad-spectrum insecticides for crops.')),
 ('agro','furrows',('أسمدة مركبة وعضوية','سماد مركب متوازن للمحاصيل.'),('Compound & Organic Fertilizers','Balanced compound fertilizer for crops.')),
]

T = {
'ar': dict(dir='rtl', locale='ar_SD', name='شركة أوتاد النخبة للتجارة المحدودة', brand='أوتاد النخبة', short='أوتاد النخبة',
 sub='للتجارة المحدودة', tagline='شريكك الموثوق في الإنتاج الحيواني والزراعي',
 desc='شركة سودانية تقدم حلولاً متكاملة في الإنتاج الحيواني والزراعي: أعلاف ومدخلات صناعة الأعلاف، وأدوية بيطرية وزراعية. نستورد المدخلات الزراعية والصناعية ونصدّر منتجاتنا إلى مختلف البلدان.',
 nav=[('index','','الرئيسية'),('about','about','من نحن'),('sectors','sectors','قطاعاتنا'),('products','products','المنتجات'),('quality','quality','الجودة'),('partners','partners','الشراكات'),('contact','contact','تواصل معنا')],
 loc='ود مدني، السودان', addr='ود مدني، ولاية الجزيرة، السودان',
 call='الهاتف', wa='واتساب', quote='اطلب عرض سعر', callnow='اتصل الآن', skip='تخطَّ إلى المحتوى', home='الرئيسية',
 hours=['السبت - الخميس: 8:00 ص - 5:00 م','الجمعة: مغلق'], openmenu='فتح القائمة', other_lang=('English','en'),
 f_sect='قطاعاتنا', f_links='روابط سريعة', f_contact='تواصل معنا', f_hours='ساعات العمل', rights='جميع الحقوق محفوظة.',
 wa_msg='مرحباً، أود الاستفسار عن منتجات أوتاد النخبة', ask='استفسر عن المنتج', more='اكتشف المزيد',
 footer_about='شركة سودانية متخصصة في الإنتاج الحيواني والزراعي، توفر الأعلاف ومدخلاتها والأدوية البيطرية والزراعية، وتعمل في الاستيراد والتصدير.'),
'en': dict(dir='ltr', locale='en_US', name='Awtad Alnokhbah Trading Co. Ltd', brand='Awtad Alnokhbah', short='Awtad Alnokhbah',
 sub='Trading Co. Ltd', tagline='Your trusted partner in livestock and agricultural production',
 desc='A Sudanese company providing integrated solutions in livestock and agricultural production: feeds and feed manufacturing inputs, veterinary medicines and agrochemicals. We import agricultural and industrial inputs and export our products to many countries.',
 nav=[('index','','Home'),('about','about','About'),('sectors','sectors','Sectors'),('products','products','Products'),('quality','quality','Quality'),('partners','partners','Partnerships'),('contact','contact','Contact')],
 loc='Wad Madani, Sudan', addr='Wad Madani, Gezira State, Sudan',
 call='Phone', wa='WhatsApp', quote='Request a quote', callnow='Call now', skip='Skip to content', home='Home',
 hours=['Saturday - Thursday: 8:00 AM - 5:00 PM','Friday: Closed'], openmenu='Open menu', other_lang=('العربية','ar'),
 f_sect='Our sectors', f_links='Quick links', f_contact='Contact', f_hours='Working hours', rights='All rights reserved.',
 wa_msg='Hello, I would like to ask about Awtad Alnokhbah products', ask='Ask about this product', more='Learn more',
 footer_about='A Sudanese company specialising in livestock and agricultural production, supplying feeds and feed inputs, veterinary medicines and agrochemicals, and active in import and export.'),
}

def P(lang, path):
    pre = '' if lang=='ar' else 'en/'
    return '/' + pre + path if (pre+path) else '/'
def other_path(lang, path): return P('en' if lang=='ar' else 'ar', path)
def waq(text): return WA + '?text=' + urllib.parse.quote(text)

FIG = {'ar':[('2026','سنة التأسيس'),('+500','عميل'),('8','ولايات نغطيها'),('6','قطاعات عمل')],
       'en':[('2026','Founded'),('500+','Clients'),('8','States covered'),('6','Business sectors')]}
def figures(lang):
    return '<ul class="figs">' + ''.join(f'<li><b><bdi>{n}</bdi></b><span>{l}</span></li>' for n,l in FIG[lang]) + '</ul>'

STATES = {'ar':['الجزيرة','الخرطوم','النيل الأبيض','النيل الأزرق','سنار','القضارف','كسلا','البحر الأحمر'],
          'en':['Gezira','Khartoum','White Nile','Blue Nile','Sennar','Gedaref','Kassala','Red Sea']}

FAQ = {
'ar':[('ما المنتجات التي توفرها أوتاد النخبة؟','نوفر أعلاف الدواجن والماشية، ومدخلات صناعة الأعلاف مثل اللايسين والمركزات البروتينية والبريمكس، والأدوية البيطرية، والمبيدات والأسمدة الزراعية.'),
      ('كيف أطلب عرض سعر؟',f'أرسل طلبك من نموذج «طلب عرض سعر» أو راسلنا على واتساب <span class="ltr">{PHONE_TXT}</span> بنوع المنتج والكمية ومكان التسليم، وسنرد عليك بالعرض.'),
      ('هل توصلون الطلبات خارج ود مدني؟','نعم، نعمل عبر شبكة توزيع تغطي ولايات الجزيرة والخرطوم والنيل الأبيض والنيل الأزرق وسنار والقضارف وكسلا والبحر الأحمر.'),
      ('هل تبيعون بالجملة للموزعين ومصانع الأعلاف؟','نعم، نورد بالجملة لمصانع الأعلاف والمزارع والموزعين، ونرحب بطلبات الموزعين المعتمدين من صفحة الشراكات.'),
      ('هل تعملون في الاستيراد والتصدير؟','نعم، نستورد المدخلات الزراعية والصناعية، ونصدّر منتجاتنا إلى مختلف البلدان. تواصل معنا لمناقشة احتياجك.'),
      ('هل تقدمون دعماً فنياً للمربين والمزارعين؟','نعم، يقدم فريقنا الإرشاد الفني حول اختيار المنتج المناسب وطريقة استخدامه.')],
'en':[('What products does Awtad Alnokhbah supply?','Poultry and cattle feeds; feed manufacturing inputs such as lysine, protein concentrates and premixes; veterinary medicines; and agricultural pesticides and fertilizers.'),
      ('How do I request a quote?',f'Use the quote request form or message us on WhatsApp at <span class="ltr">{PHONE_TXT}</span> with the product, quantity and delivery location, and we will reply with an offer.'),
      ('Do you deliver outside Wad Madani?','Yes. Our distribution network covers Gezira, Khartoum, White Nile, Blue Nile, Sennar, Gedaref, Kassala and Red Sea states.'),
      ('Do you sell wholesale to distributors and feed mills?','Yes. We supply feed mills, farms and distributors in bulk, and welcome distributor applications through the Partnerships page.'),
      ('Are you active in import and export?','Yes. We import agricultural and industrial inputs and export our products to many countries. Contact us to discuss your needs.'),
      ('Do you provide technical support to breeders and farmers?','Yes. Our team gives technical guidance on choosing the right product and how to use it.')],
}

FONTS = 'family=Readex+Pro:wght@400;500;600&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700'

def ld(lang, key, title, path):
    t=T[lang]
    org={"@type":["Organization","LocalBusiness"],"@id":DOMAIN+"/#org","name":T['ar']['name'],"alternateName":[T['en']['name'],"أوتاد النخبة","Awtad Alnokhbah","Awtad"],
         "url":DOMAIN+"/","logo":DOMAIN+"/assets/img/logo.png","image":DOMAIN+"/assets/img/og.jpg",
         "telephone":"+"+PHONE,"email":EMAIL,"description":t['desc'],"foundingDate":"2026",
         "address":{"@type":"PostalAddress","addressLocality":"ود مدني" if lang=='ar' else "Wad Madani","addressRegion":"الجزيرة" if lang=='ar' else "Gezira","addressCountry":"SD"},
         "areaServed":[{"@type":"Country","name":"السودان" if lang=='ar' else "Sudan"}],
         "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Saturday","Sunday","Monday","Tuesday","Wednesday","Thursday"],"opens":"08:00","closes":"17:00"}],
         "knowsAbout":[s[lang][0] for s in SECT],
         "contactPoint":[{"@type":"ContactPoint","telephone":"+"+PHONE,"contactType":"sales","availableLanguage":["Arabic","English"]}]}
    g=[org]
    if key=='index':
        g.append({"@type":"WebSite","url":DOMAIN+P(lang,''),"name":t['name'],"inLanguage":lang})
        g.append({"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in FAQ[lang]]})
    else:
        items=[{"@type":"ListItem","position":1,"name":t['home'],"item":DOMAIN+P(lang,'')},
               {"@type":"ListItem","position":2,"name":title.split(' | ')[0],"item":DOMAIN+path}]
        g.append({"@type":"BreadcrumbList","itemListElement":items})
        if key=='products':
            g.append({"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"Product","name":p[2 if lang=='ar' else 3][0],"description":p[2 if lang=='ar' else 3][1],"image":DOMAIN+f"/assets/img/{p[1]}.webp","brand":{"@id":DOMAIN+"/#org"}}} for i,p in enumerate(PROD)]})
    return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@graph":g},ensure_ascii=False)+'</script>'

def page(lang, key, rel, title, desc, body, noindex=False):
    t=T[lang]; path=P(lang,rel); url=DOMAIN+path
    nav=''.join(f'<li><a href="{P(lang,h)}"{" aria-current=\"page\"" if k==key else ""}>{n}</a></li>' for k,h,n in t['nav'])
    olbl, olang = t['other_lang']
    alt = '' if noindex else (f'<link rel="alternate" hreflang="ar" href="{DOMAIN}{P("ar",rel)}">\n'
          f'<link rel="alternate" hreflang="en" href="{DOMAIN}{P("en",rel)}">\n'
          f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}{P("ar",rel)}">')
    fsect=''.join(f'<li><a href="{P(lang,"sectors")}#{s["id"]}">{s[lang][0]}</a></li>' for s in SECT)
    return f'''<!doctype html>
<html lang="{lang}" dir="{t['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="canonical" href="{url}">
{alt}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{t['name']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/img/og.jpg">
<meta property="og:locale" content="{t['locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#363D1C">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{FONTS}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{'' if noindex else ld(lang,key,title,path)}
</head>
<body>
<a class="skip" href="#main">{t['skip']}</a>
<div class="topbar"><div class="wrap">
  <div class="grp"><a href="tel:+{PHONE}">{t['call']}: <span class="ltr">{PHONE_TXT}</span></a><a class="mail" href="mailto:{EMAIL}">{EMAIL}</a></div>
  <div class="grp"><span class="loc">{t['loc']}</span><a class="lang" href="{other_path(lang,'' if noindex else rel)}" lang="{olang}" hreflang="{olang}">{olbl}</a></div>
</div></div>
<header class="site"><div class="wrap">
  <a class="brand" href="{P(lang,'')}" aria-label="{t['name']}"><img src="/assets/img/logo.webp" alt="{t['name']}" width="64" height="62"><span class="bn"><b>{t['brand']}</b><span>{t['sub']}</span></span></a>
  <nav class="main" id="nav" aria-label="{t['nav'][0][2]}"><ul>{nav}</ul></nav>
  <a class="btn btn-green head-cta" href="{P(lang,'contact')}#quote">{t['quote']}</a>
  <button class="menu-btn" aria-controls="nav" aria-expanded="false" aria-label="{t['openmenu']}">{I['menu']}</button>
</div></header>
<main id="main">
{body}
</main>
<footer class="site">
  <div class="wrap">
    <div><a class="flogo" href="{P(lang,'')}"><img src="/assets/img/logo.webp" alt="{t['name']}" width="76" height="74"></a><p>{t['footer_about']}</p></div>
    <div><h4>{t['f_sect']}</h4><ul>{fsect}</ul></div>
    <div><h4>{t['f_links']}</h4><ul>{''.join(f'<li><a href="{P(lang,h)}">{n}</a></li>' for k,h,n in t['nav'])}</ul></div>
    <div><h4>{t['f_contact']}</h4><ul>
      <li>{t['call']}: <a href="tel:+{PHONE}"><span class="ltr">{PHONE_TXT}</span></a></li>
      <li>{t['wa']}: <a href="{waq(t['wa_msg'])}" target="_blank" rel="noopener"><span class="ltr">{PHONE_TXT}</span></a></li>
      <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li>{t['addr']}</li>
      <li>{t['hours'][0]}</li><li>{t['hours'][1]}</li></ul></div>
  </div>
  <div class="fbar"><div class="wrap">
    <span>© <span id="yr">2026</span> {t['name']}. {t['rights']}</span>
    <span>{t['loc']}</span>
  </div></div>
</footer>
<a class="wa-float" href="{waq(t['wa_msg'])}" target="_blank" rel="noopener" aria-label="{t['wa']}">{WA_SVG}</a>
<script src="/assets/site.js" defer></script>
</body>
</html>'''

def head(lang, eb, h, p=None):
    return f'<div class="sec-head"><span class="eyebrow">{SLAB}{eb}</span><h2>{h}</h2>{f"<p>{p}</p>" if p else ""}</div>'

def phead(lang, title, sub, crumb, img):
    t=T[lang]
    return f'''<section class="phead" style="background-image:url('/assets/img/{img}.webp')"><div class="wrap">
<div class="crumbs"><a href="{P(lang,"")}">{t["home"]}</a> / {crumb}</div>
<h1>{title}</h1><p>{sub}</p></div></section>'''

def sector_cards(lang):
    t=T[lang]; out=''
    for i,s in enumerate(SECT,1):
        n,d=s[lang][0],s[lang][1]
        out+=f'''<a class="sector" href="{P(lang,'sectors')}#{s['id']}"><div class="ph"><img src="/assets/img/{s['img']}.webp" alt="{n}" loading="lazy"></div><span class="no">{i:02d}</span>
<div class="bd"><h3>{n}</h3><p>{d}</p><span class="go">{t['more']}</span></div></a>'''
    return f'<div class="sectors">{out}</div>'

def prod_cards(lang, items=None, chips=False, full=False):
    t=T[lang]; a=lang=='ar'; out=''
    for cat,img,ar,en in (items or PROD):
        n,d=(ar if a else en); c=CATS[cat][0 if a else 1]
        out+=f'''<article class="prod" data-cat="{cat}"><div class="ph"><img src="/assets/img/{img}.webp" alt="{n}" loading="lazy"></div>
<div class="bd"><span class="cat">{c}</span><h3>{n}</h3><p>{d}</p><a class="ask" href="{waq(t['wa_msg']+(' - ' if a else ' - ')+n)}" target="_blank" rel="noopener">{WA_SVG}{t['ask']}</a></div></article>'''
    ch=''
    if chips:
        ch='<div class="chips" role="group" aria-label="'+('تصنيف المنتجات' if a else 'Filter products')+'"><button type="button" data-f="all" aria-pressed="true">'+('الكل' if a else 'All')+'</button>'+''.join(f'<button type="button" data-f="{k}" aria-pressed="false">{v[0 if a else 1]}</button>' for k,v in CATS.items())+'</div>'
    return ch+f'<div class="products{" full" if full else ""}">{out}</div>'

FEATS = {
'ar':[('badge','جودة موثوقة','منتجات مختارة من موردين موثوقين، تُفحص وتُخزّن وفق معايير الجودة.'),
      ('users','ثقة أكثر من 500 عميل','مزارعون ومربون وموزعون يعتمدون على منتجاتنا وخدماتنا.'),
      ('truck','توزيع في 8 ولايات','شبكة توزيع تصل إلى المزارع والموزعين في وقت مناسب.'),
      ('globe','استيراد وتصدير','نستورد المدخلات الزراعية والصناعية ونصدّر منتجاتنا إلى مختلف البلدان.'),
      ('chat','دعم فني متخصص','فريق يقدم الإرشاد حول اختيار المنتج وطريقة استخدامه.'),
      ('leaf','أسعار تنافسية','عروض أسعار واضحة تناسب المزارع الصغيرة والمشاريع الكبيرة.')],
'en':[('badge','Reliable quality','Products from trusted suppliers, inspected and stored to quality standards.'),
      ('users','Trusted by 500+ clients','Farmers, breeders and distributors rely on our products and service.'),
      ('truck','Distribution in 8 states','A distribution network that reaches farms and distributors on time.'),
      ('globe','Import and export','We import agricultural and industrial inputs and export our products to many countries.'),
      ('chat','Specialist technical support','A team that advises on choosing the right product and how to use it.'),
      ('leaf','Competitive prices','Clear quotes that suit small farms and large projects alike.')],
}
def feats(lang):
    return '<div class="feats">'+''.join(f'<div class="feat"><div class="ic">{I[i]}</div><div><h3>{h}</h3><p>{d}</p></div></div>' for i,h,d in FEATS[lang])+'</div>'

STEPS = {'ar':[('أرسل طلبك','حدّد المنتج والكمية ومكان التسليم عبر النموذج أو واتساب.'),('نرسل العرض','نجهز لك عرض سعر واضحاً ومواعيد التوريد.'),('التأكيد والتجهيز','بعد التأكيد نجهز الطلب من مخازننا.'),('التسليم والمتابعة','نوصل الطلب ونتابع معك بالإرشاد الفني.')],
         'en':[('Send your request','Tell us the product, quantity and delivery location by form or WhatsApp.'),('We send a quote','We prepare a clear price offer and supply schedule.'),('Confirm and prepare','Once confirmed, we prepare your order from our stores.'),('Delivery and follow-up','We deliver and follow up with technical guidance.')]}
def steps(lang): return '<div class="steps">'+''.join(f'<div><h3>{h}</h3><p>{d}</p></div>' for h,d in STEPS[lang])+'</div>'
def faq(lang): return '<div class="faq">'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQ[lang])+'</div>'

def trade(lang):
    a=lang=='ar'
    return f'''<div class="trade">
<div><span class="dir">{'الاستيراد' if a else 'Import'}</span><h3>{'مدخلات زراعية وصناعية' if a else 'Agricultural and industrial inputs'}</h3>
<p>{'نستورد مدخلات صناعة الأعلاف والمدخلات الزراعية والصناعية من موردين في الخارج، لنوفرها للمصانع والمزارع والموزعين في السودان.' if a else 'We import feed manufacturing inputs and agricultural and industrial inputs from overseas suppliers, supplying them to mills, farms and distributors in Sudan.'}</p></div>
<div><span class="dir">{'التصدير' if a else 'Export'}</span><h3>{'منتجات سودانية إلى الخارج' if a else 'Sudanese products abroad'}</h3>
<p>{'نصدّر منتجاتنا إلى مختلف البلدان. إذا كنت مستورداً أو موزعاً خارج السودان، تواصل معنا لمناقشة الكميات والشروط.' if a else 'We export our products to many countries. If you are an importer or distributor outside Sudan, contact us to discuss quantities and terms.'}</p></div>
</div>'''

def quote_form(lang):
    a=lang=='ar'
    opts=''.join(f'<option>{s[lang][0]}</option>' for s in SECT)+('<option>استيراد / تصدير</option><option>أخرى</option>' if a else '<option>Import / export</option><option>Other</option>')
    return f'''<form class="wa formcard" id="quoteForm" novalidate>
<h2 id="quote" style="font-size:1.45rem;scroll-margin-top:110px">{'طلب عرض سعر' if a else 'Request a quote'}</h2>
<div class="row2">
<div class="f"><label for="qn">{'الاسم الكامل' if a else 'Full name'}</label><input id="qn" required autocomplete="name"></div>
<div class="f"><label for="qp">{'رقم الهاتف' if a else 'Phone number'}</label><input id="qp" type="tel" required autocomplete="tel" dir="ltr"></div>
</div>
<div class="row2">
<div class="f"><label for="qs">{'القطاع' if a else 'Sector'}</label><select id="qs">{opts}</select></div>
<div class="f"><label for="qq">{'الكمية التقريبية (اختياري)' if a else 'Approx. quantity (optional)'}</label><input id="qq"></div>
</div>
<div class="f"><label for="qm">{'تفاصيل الطلب ومكان التسليم' if a else 'Order details and delivery location'}</label><textarea id="qm" rows="4"></textarea></div>
<div class="err" id="quoteErr" role="alert"></div>
<button class="btn btn-wa" type="submit">{WA_SVG}{'إرسال الطلب عبر واتساب' if a else 'Send via WhatsApp'}</button>
<p class="note">{'يفتح واتساب ورسالتك جاهزة للإرسال.' if a else 'WhatsApp opens with your request ready to send.'}</p>
</form>'''

def partner_form(lang):
    a=lang=='ar'
    types=(['مورد أعلاف','مورد أدوية بيطرية','موزع معتمد','شراكة استراتيجية','مستورد من خارج السودان'] if a else ['Feed supplier','Veterinary medicines supplier','Authorised distributor','Strategic partnership','Importer outside Sudan'])
    return f'''<form class="wa formcard" id="partnerForm" novalidate>
<h2 style="font-size:1.45rem">{'كن شريكنا' if a else 'Become a partner'}</h2>
<div class="row2">
<div class="f"><label for="pc">{'اسم الشركة / المؤسسة' if a else 'Company / organisation'}</label><input id="pc" required autocomplete="organization"></div>
<div class="f"><label for="pn">{'اسم المسؤول' if a else 'Contact person'}</label><input id="pn" required autocomplete="name"></div>
</div>
<div class="row2">
<div class="f"><label for="pp">{'رقم الهاتف' if a else 'Phone number'}</label><input id="pp" type="tel" required autocomplete="tel" dir="ltr"></div>
<div class="f"><label for="pt">{'نوع الشراكة' if a else 'Partnership type'}</label><select id="pt">{''.join(f'<option>{x}</option>' for x in types)}</select></div>
</div>
<div class="f"><label for="pm">{'تفاصيل إضافية (اختياري)' if a else 'Additional details (optional)'}</label><textarea id="pm" rows="4"></textarea></div>
<div class="err" id="partnerErr" role="alert"></div>
<button class="btn btn-wa" type="submit">{WA_SVG}{'إرسال طلب الشراكة عبر واتساب' if a else 'Send via WhatsApp'}</button>
</form>'''

def info_box(lang):
    t=T[lang]; a=lang=='ar'
    return f'''<aside class="info"><h2>{'معلومات التواصل' if a else 'Contact details'}</h2><dl>
<dt>{'الهاتف وواتساب' if a else 'Phone & WhatsApp'}</dt><dd><a href="tel:+{PHONE}"><span class="ltr">{PHONE_TXT}</span></a><br><a href="{waq(t['wa_msg'])}" target="_blank" rel="noopener">{'راسلنا على واتساب' if a else 'Message us on WhatsApp'}</a></dd>
<dt>{'البريد الإلكتروني' if a else 'Email'}</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
<dt>{'العنوان' if a else 'Address'}</dt><dd>{t['addr']}<br><a href="{MAP_LINK}" target="_blank" rel="noopener">{'افتح على خرائط Google' if a else 'Open in Google Maps'}</a></dd>
<dt>{t['f_hours']}</dt><dd>{t['hours'][0]}<br>{t['hours'][1]}</dd>
</dl></aside>'''

def cta(lang):
    t=T[lang]; a=lang=='ar'
    return f'''<section class="cta"><div class="wrap"><div><h2>{'تبحث عن شريك موثوق في قطاعك الزراعي؟' if a else 'Looking for a reliable partner in agriculture?'}</h2>
<p>{'تواصل معنا اليوم واحصل على عرض سعر واستشارة فنية من فريقنا.' if a else 'Contact us today for a quote and technical advice from our team.'}</p></div>
<div class="acts"><a class="btn btn-olive" href="{P(lang,'contact')}#quote">{t['quote']}</a><a class="btn btn-line" href="{waq(t['wa_msg'])}" target="_blank" rel="noopener">{WA_SVG}{t['wa']}</a></div></div></section>'''

TEAM = [('team-abdalmahmoud',('د. عبدالمحمود الشيخ','رئيس مجلس الإدارة والمدير التنفيذي'),('Dr. Abdalmahmoud Elshiekh','Chairman & CEO')),
        ('team-taymour',('تيمور حمزة','مدير التقنية'),('Taymour Hamza','Chief Technology Officer'))]

# ---------------- الصفحات ----------------
def home(lang):
    t=T[lang]; a=lang=='ar'
    return f'''<section class="hero"><img src="/assets/img/hero.webp" alt="{'مزارعون في حقل حصاد في السودان' if a else 'Farmers at a harvest field in Sudan'}" width="1600" height="1067" fetchpriority="high"><div class="wrap"><div class="in">
<span class="kicker">{SLAB}{'الريادة في القطاع الزراعي والحيواني' if a else 'Leading in agriculture and livestock'}</span>
<h1>{'شركة أوتاد النخبة <em>للتجارة</em>' if a else 'Awtad Alnokhbah <em>Trading</em>'}</h1>
<p class="en-name">{'Awtad Alnokhbah Trading Co. Ltd' if a else 'شركة أوتاد النخبة للتجارة المحدودة'}</p>
<p class="sub">{'أعلاف، ومدخلات صناعة الأعلاف، وأدوية بيطرية وزراعية للمزارعين والمربين في السودان، مع خدمات الاستيراد والتصدير.' if a else 'Feeds, feed manufacturing inputs, veterinary medicines and agrochemicals for farmers and breeders in Sudan, plus import and export services.'}</p>
<div class="acts"><a class="btn btn-green" href="{P(lang,'products')}">{'تصفح المنتجات' if a else 'Browse products'}</a><a class="btn btn-line" href="{waq(t['wa_msg'])}" target="_blank" rel="noopener">{WA_SVG}{t['wa']}</a></div>
</div></div><div class="cut" aria-hidden="true"></div></section>
<div class="figs-band"><div class="wrap">{figures(lang)}</div></div>

<section class="blk"><div class="wrap">
{head(lang,'قطاعات العمل' if a else 'Business sectors','مجالات تخصصنا' if a else 'What we specialise in','حلول متكاملة في قطاعات الإنتاج الحيواني والزراعي.' if a else 'Integrated solutions across livestock and agricultural production.')}
{sector_cards(lang)}
</div></section>

<section class="blk sand"><div class="wrap split">
<div><span class="eyebrow">{SLAB}{'من نحن' if a else 'About us'}</span>
<h2>{t['name']}</h2>
<p>{'شركة سودانية متخصصة في مجال الإنتاج الحيواني والزراعي، تأسست عام 2026 في ود مدني لتقديم أفضل المنتجات والخدمات للمزارعين والمربين في أنحاء السودان.' if a else 'A Sudanese company specialising in livestock and agricultural production, founded in 2026 in Wad Madani to provide farmers and breeders across Sudan with the best products and services.'}</p>
<p>{'نوفر الأعلاف ومدخلات صناعتها والأدوية البيطرية والزراعية، ونستورد المدخلات الزراعية والصناعية ونصدّر منتجاتنا إلى مختلف البلدان.' if a else 'We supply feeds and their manufacturing inputs, veterinary medicines and agrochemicals; we import agricultural and industrial inputs and export our products to many countries.'}</p>
<ul class="checks">{''.join(f'<li>{x}</li>' for x in (['جودة موثوقة','أسعار تنافسية','دعم فني متخصص','توزيع في 8 ولايات'] if a else ['Reliable quality','Competitive prices','Specialist support','Distribution in 8 states']))}</ul>
<a class="btn btn-olive" href="{P(lang,'about')}">{'اعرف المزيد عنا' if a else 'More about us'}</a></div>
<img src="/assets/img/hq.webp" alt="{t['name']}" loading="lazy">
</div></section>

<section class="blk"><div class="wrap">
{head(lang,'منتجاتنا' if a else 'Our products','من منتجاتنا' if a else 'Featured products','أعلاف ومدخلات وأدوية بيطرية وزراعية. اضغط «استفسر عن المنتج» لتصلنا رسالتك على واتساب.' if a else 'Feeds, inputs, veterinary medicines and agrochemicals. Tap “Ask about this product” to message us on WhatsApp.')}
{prod_cards(lang, [PROD[0],PROD[1],PROD[4],PROD[5],PROD[6],PROD[7],PROD[9],PROD[10]])}
<p style="margin-top:28px"><a class="btn btn-ghost" href="{P(lang,'products')}">{'عرض جميع المنتجات' if a else 'View all products'}</a></p>
</div></section>

<section class="blk dark"><div class="wrap">
{head(lang,'التجارة الخارجية' if a else 'International trade','استيراد وتصدير' if a else 'Import and export','نربط السوق السوداني بالموردين في الخارج، ونوصل منتجاتنا إلى أسواق جديدة.' if a else 'We connect the Sudanese market with overseas suppliers and take our products to new markets.')}
{trade(lang)}
</div></section>

<section class="blk"><div class="wrap">
{head(lang,'لماذا أوتاد النخبة؟' if a else 'Why Awtad Alnokhbah?','مميزاتنا' if a else 'What sets us apart')}
{feats(lang)}
</div></section>

<section class="blk sand"><div class="wrap">
{head(lang,'كيف نعمل' if a else 'How it works','من الطلب إلى التسليم' if a else 'From request to delivery')}
{steps(lang)}
</div></section>

<section class="blk"><div class="wrap">
{head(lang,'الأسئلة الشائعة' if a else 'FAQ','أسئلة متكررة' if a else 'Frequently asked questions')}
{faq(lang)}
</div></section>
{cta(lang)}'''

def about_page(lang):
    t=T[lang]; a=lang=='ar'
    vals=[('الجودة','نلتزم بأعلى معايير الجودة في جميع منتجاتنا وخدماتنا.'),('الاستدامة','نسعى لتحقيق التنمية المستدامة في القطاع الزراعي.'),('دعم المزارع','نقدم الدعم الفني والإرشادي للمزارعين والمربين.'),('الأمانة','نتعامل بشفافية وأمانة مع جميع شركائنا.')] if a else \
         [('Quality','We hold all our products and services to the highest quality standards.'),('Sustainability','We work towards sustainable development in agriculture.'),('Farmer support','We give technical and advisory support to farmers and breeders.'),('Integrity','We deal transparently and honestly with all our partners.')]
    st=''.join(f'<li class="hq">{x}</li>' if i==0 else f'<li>{x}</li>' for i,x in enumerate(STATES[lang]))
    team=''.join(f'<div class="member"><div class="ph"><img src="/assets/img/{img}.webp" alt="{(ar if a else en)[0]}" loading="lazy"></div><h3>{(ar if a else en)[0]}</h3><span>{(ar if a else en)[1]}</span></div>' for img,ar,en in TEAM)
    return phead(lang,'من نحن' if a else 'About us','تعرف على شركة أوتاد النخبة للتجارة المحدودة.' if a else 'Get to know Awtad Alnokhbah Trading Co. Ltd.','من نحن' if a else 'About','field') + f'''
<section class="blk"><div class="wrap split">
<div><span class="eyebrow">{SLAB}{'قصتنا' if a else 'Our story'}</span>
<h2>{'نبذة عن الشركة' if a else 'Company profile'}</h2>
<p>{'تأسست شركة أوتاد النخبة للتجارة المحدودة في السودان عام 2026 بهدف تقديم حلول متكاملة في مجال الإنتاج الحيواني والزراعي، وتسعى لتكون الشريك الموثوق للمزارعين والمربين في جميع أنحاء السودان.' if a else 'Awtad Alnokhbah Trading Co. Ltd was founded in Sudan in 2026 to provide integrated solutions in livestock and agricultural production, and aims to be the trusted partner of farmers and breeders across Sudan.'}</p>
<p>{'نقدم مجموعة واسعة من المنتجات تشمل الأعلاف بأنواعها، ومدخلات صناعة الأعلاف، والأدوية البيطرية والزراعية، ونستورد المدخلات الزراعية والصناعية ونصدّر منتجاتنا إلى مختلف البلدان.' if a else 'Our range covers all types of feed, feed manufacturing inputs, veterinary medicines and agrochemicals. We import agricultural and industrial inputs and export our products to many countries.'}</p>
<p>{'اسم «أوتاد» يرمز إلى الثبات والنمو، وهو ما نسعى لتحقيقه مع شركائنا من المزارعين والمربين لبناء قطاع زراعي مستدام ومزدهر.' if a else 'The name “Awtad” (pegs) stands for stability and growth, which is what we aim to build with our farmer and breeder partners: a sustainable, thriving agricultural sector.'}</p>
</div>
<img src="/assets/img/hq.webp" alt="{t['name']}" loading="lazy">
</div></section>
<section class="blk sand"><div class="wrap">
<div class="vm">
<div><h3>{'رؤيتنا' if a else 'Our vision'}</h3><p>{'أن نكون الشركة الرائدة في مجال الإنتاج الحيواني والزراعي في السودان والمنطقة، ونساهم في تحقيق الأمن الغذائي والتنمية المستدامة.' if a else 'To be the leading livestock and agricultural production company in Sudan and the region, contributing to food security and sustainable development.'}</p></div>
<div><h3>{'رسالتنا' if a else 'Our mission'}</h3><p>{'تقديم منتجات وخدمات عالية الجودة تلبي احتياجات المزارعين والمربين، مع الالتزام بمعايير الجودة والاستدامة، ودعم التنمية الزراعية في السودان.' if a else 'To deliver high-quality products and services that meet the needs of farmers and breeders, committed to quality and sustainability, and supporting agricultural development in Sudan.'}</p></div>
</div></div></section>
<section class="blk"><div class="wrap">
{head(lang,'قيمنا' if a else 'Our values','القيم المؤسسية' if a else 'Corporate values','القيم التي نؤمن بها وتوجه عملنا.' if a else 'The values we believe in and that guide our work.')}
<div class="vals">{''.join(f'<div><h3>{h}</h3><p>{d}</p></div>' for h,d in vals)}</div>
</div></section>
<section class="blk dark"><div class="wrap leader">
<img src="/assets/img/team-abdalmahmoud.webp" alt="{TEAM[0][1 if a else 2][0]}" loading="lazy">
<div><span class="eyebrow">{SLAB}{'كلمة الإدارة' if a else 'A word from the chairman'}</span>
<blockquote><p>{'«نؤمن في شركة أوتاد النخبة للتجارة المحدودة بأن نجاحنا مرتبط بنجاح شركائنا من المزارعين والمربين. لذلك نسعى دائماً لتقديم أفضل المنتجات والخدمات التي تساعدهم على تحقيق أهدافهم.' if a else '“At Awtad Alnokhbah Trading we believe our success is tied to the success of our farmer and breeder partners. That is why we always strive to offer the products and services that help them reach their goals.'}</p>
<p>{'نلتزم بالجودة والابتكار والاستدامة في كل ما نقدمه، ونعمل باستمرار على تطوير منتجاتنا وخدماتنا لتلبية احتياجات السوق المتغيرة.»' if a else 'We are committed to quality, innovation and sustainability in everything we offer, and we keep developing our products and services to meet a changing market.”'}</p></blockquote>
<cite><b>{TEAM[0][1 if a else 2][0]}</b><span>{TEAM[0][1 if a else 2][1]}</span></cite></div>
</div></section>
<section class="blk" id="team" style="scroll-margin-top:90px"><div class="wrap">
{head(lang,'القيادة' if a else 'Leadership','فريق العمل' if a else 'Our team','متخصصون في الإنتاج الحيواني والزراعي والتجارة، نعمل لتقديم أفضل قيمة لعملائنا وشركائنا.' if a else 'Specialists in livestock, agriculture and trade, working to deliver the best value to our clients and partners.')}
<div class="team">{team}</div>
</div></section>
<section class="blk sand"><div class="wrap">
{head(lang,'التغطية الجغرافية' if a else 'Geographic coverage','مناطق العمل' if a else 'Where we work','مقرنا في ود مدني بولاية الجزيرة، وشبكة توزيعنا تغطي 8 ولايات.' if a else 'Headquartered in Wad Madani, Gezira State, with a distribution network covering 8 states.')}
<ul class="states">{st}</ul>
</div></section>
{cta(lang)}'''

def sectors_page(lang):
    t=T[lang]; a=lang=='ar'; rows=''
    for i,s in enumerate(SECT,1):
        n,d,long,inc=s[lang]
        rows+=f'''<div class="sector-row" id="{s['id']}"><div class="ph"><img src="/assets/img/{s['img']}.webp" alt="{n}" loading="lazy"></div>
<div><span class="n">{i:02d}</span><h2>{n}</h2><p>{long}</p><ul class="checks">{''.join(f'<li>{x}</li>' for x in inc)}</ul>
<a class="btn btn-green" href="{waq(t['wa_msg']+' - '+n)}" target="_blank" rel="noopener">{WA_SVG}{'استفسر عن هذا القطاع' if a else 'Ask about this sector'}</a></div></div>'''
    return phead(lang,'قطاعات العمل' if a else 'Business sectors','مجالات تخصصنا في الإنتاج الحيواني والزراعي.' if a else 'Our areas of specialisation in livestock and agricultural production.','قطاعاتنا' if a else 'Sectors','cattle') + f'''
<section class="blk"><div class="wrap">{sector_cards(lang)}</div></section>
<section class="blk" style="padding-top:0"><div class="wrap">{rows}</div></section>
<section class="blk dark"><div class="wrap">
{head(lang,'التجارة الخارجية' if a else 'International trade','استيراد وتصدير' if a else 'Import and export')}
{trade(lang)}
</div></section>
{cta(lang)}'''

def products_page(lang):
    a=lang=='ar'
    return phead(lang,'المنتجات' if a else 'Products','تصفح مجموعتنا من الأعلاف ومدخلات صناعتها والأدوية البيطرية والزراعية.' if a else 'Browse our feeds, feed inputs, veterinary medicines and agrochemicals.','المنتجات' if a else 'Products','p-pellets') + f'''
<section class="blk sand"><div class="wrap">
{prod_cards(lang, chips=True, full=True)}
<p style="margin-top:30px;color:var(--muted)">{'لا تجد المنتج الذي تبحث عنه؟ أرسل لنا طلبك وسنوفره لك.' if a else 'Can’t find what you need? Send us your request and we will source it.'} <a href="{P(lang,'contact')}#quote" style="color:var(--green);font-weight:600">{T[lang]['quote']}</a></p>
</div></section>
{cta(lang)}'''

def quality_page(lang):
    a=lang=='ar'
    q=[('shield','ضمان الجودة','نلتزم بمعايير الجودة في جميع مراحل التوريد والتخزين والتوزيع.'),('flask','الفحص والاختبار','نختار المنتجات من موردين موثوقين ونتحقق من مطابقتها للمواصفات قبل طرحها.'),('list','التوثيق والتتبع','نوثق الشحنات بما يسمح بتتبع المنتج من المصدر إلى العميل.'),('refresh','التحسين المستمر','نطور منتجاتنا وعملياتنا باستمرار بناءً على ملاحظات العملاء.')] if a else \
      [('shield','Quality assurance','We apply quality standards at every stage of supply, storage and distribution.'),('flask','Inspection and testing','We source from trusted suppliers and check products against specifications before release.'),('list','Documentation and traceability','We document shipments so products can be traced from source to customer.'),('refresh','Continuous improvement','We keep improving our products and processes based on customer feedback.')]
    ctrl=(['فحص المواد عند الاستلام','مراقبة ظروف التخزين','اختبارات جودة دورية','التحقق من مطابقة المواصفات','مراجعة شكاوى العملاء والتحسين','تدريب الموظفين على معايير الجودة'] if a else
          ['Inspection on receipt','Monitoring storage conditions','Periodic quality checks','Verifying conformity to specifications','Reviewing customer complaints and improving','Training staff on quality standards'])
    return phead(lang,'الجودة' if a else 'Quality','التزامنا بالجودة من استلام المنتج حتى تسليمه.' if a else 'Our commitment to quality from receipt to delivery.','الجودة' if a else 'Quality','tubes') + f'''
<section class="blk"><div class="wrap">
{head(lang,'سياسة الجودة' if a else 'Quality policy','التزامنا بالجودة' if a else 'Our commitment to quality','نؤمن بأن الجودة أساس نجاحنا ورضا عملائنا.' if a else 'We believe quality is the foundation of our success and our clients’ satisfaction.')}
<div class="qgrid">{''.join(f'<div><div class="ic">{I[i]}</div><h3>{h}</h3><p>{d}</p></div>' for i,h,d in q)}</div>
</div></section>
<section class="blk sand"><div class="wrap split">
<div><span class="eyebrow">{SLAB}{'إجراءات الرقابة' if a else 'Control procedures'}</span>
<h2>{'نظام الرقابة على الجودة' if a else 'Quality control system'}</h2>
<p>{'نطبق رقابة على الجودة تشمل مراحل العمل كلها، من استلام المنتجات وحتى تسليمها للعميل.' if a else 'Our quality control covers every stage of our work, from receiving products to delivering them to the customer.'}</p>
<ul class="checks">{''.join(f'<li>{x}</li>' for x in ctrl)}</ul>
<p style="color:var(--muted)">{'ونلتزم بالمعايير البيطرية والزراعية المعتمدة في السودان والمنطقة في كل ما نوفره من منتجات.' if a else 'We follow the veterinary and agricultural standards applicable in Sudan and the region for every product we supply.'}</p></div>
<img src="/assets/img/lab.webp" alt="{'مختبر فحص الجودة' if a else 'Quality testing laboratory'}" loading="lazy" style="aspect-ratio:4/5">
</div></section>
{cta(lang)}'''

def partners_page(lang):
    a=lang=='ar'
    pt=[('موردو الأعلاف','نتعاون مع موردي الأعلاف ومكوناتها عالية الجودة من مختلف أنحاء العالم.',['معايير جودة عالية','إمدادات منتظمة','أسعار تنافسية']),
        ('موردو الأدوية البيطرية','نتعاون مع مصنّعي الأدوية البيطرية والزراعية المرخّصين لضمان سلامة المنتجات.',['منتجات مرخّصة','ضمان الأصالة','دعم فني']),
        ('شركاء التوزيع','نبني شبكة موزعين في الولايات لضمان وصول منتجاتنا في الوقت المناسب.',['تغطية جغرافية واسعة','توصيل سريع','خدمة ما بعد البيع']),
        ('شراكات استراتيجية','نرحب بالشراكات مع الجهات الحكومية والمنظمات الزراعية والمستوردين من خارج السودان.',['مشاريع مشتركة','حلول مخصصة','دعم مؤسسي'])] if a else \
       [('Feed suppliers','We work with suppliers of high-quality feeds and feed ingredients from around the world.',['High quality standards','Regular supply','Competitive prices']),
        ('Veterinary suppliers','We work with licensed manufacturers of veterinary medicines and agrochemicals to ensure product safety.',['Licensed products','Guaranteed authenticity','Technical support']),
        ('Distribution partners','We are building a network of distributors across the states so our products arrive on time.',['Wide coverage','Fast delivery','After-sales service']),
        ('Strategic partnerships','We welcome partnerships with government bodies, agricultural organisations and importers outside Sudan.',['Joint projects','Tailored solutions','Institutional support'])]
    return phead(lang,'الشراكات' if a else 'Partnerships','نماذج شراكة متعددة تناسب الجهات والشركات العاملة في القطاع الزراعي والحيواني.' if a else 'Partnership models for organisations and companies in agriculture and livestock.','الشراكات' if a else 'Partnerships','handshake') + f'''
<section class="blk"><div class="wrap">
{head(lang,'فرص الشراكة' if a else 'Partnership opportunities','أنواع الشراكات' if a else 'Types of partnership')}
<div class="ptypes">{''.join(f'<div><h3>{h}</h3><p>{d}</p><ul class="checks">{"".join(f"<li>{x}</li>" for x in l)}</ul></div>' for h,d,l in pt)}</div>
</div></section>
<section class="blk sand"><div class="wrap contact-grid">
{partner_form(lang)}
{info_box(lang)}
</div></section>'''

def contact_page(lang):
    a=lang=='ar'
    return phead(lang,'تواصل معنا' if a else 'Contact us','نحن هنا لمساعدتك. أرسل طلبك أو اتصل بنا مباشرة.' if a else 'We are here to help. Send your request or call us directly.','تواصل معنا' if a else 'Contact','support') + f'''
<section class="blk"><div class="wrap contact-grid">
<div>{quote_form(lang)}
<div class="map"><iframe src="{MAP_EMBED}" title="{'موقعنا في ود مدني' if a else 'Our location in Wad Madani'}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div></div>
{info_box(lang)}
</div></section>'''

def notfound(lang):
    a=lang=='ar'
    return phead(lang,'الصفحة غير موجودة' if a else 'Page not found','الرابط الذي فتحته غير صحيح أو تم نقله.' if a else 'The link you opened is wrong or has moved.','404','field') + f'''
<section class="blk"><div class="wrap"><a class="btn btn-olive" href="{P(lang,'')}">{'العودة إلى الصفحة الرئيسية' if a else 'Back to home'}</a></div></section>'''

TITLES = {
'ar': dict(index=('أوتاد النخبة للتجارة | أعلاف وأدوية بيطرية وزراعية في السودان','شركة أوتاد النخبة للتجارة المحدودة في ود مدني: أعلاف الدواجن والماشية، مدخلات صناعة الأعلاف، أدوية بيطرية ومبيدات وأسمدة زراعية، استيراد وتصدير. +500 عميل.'),
           about=('من نحن | أوتاد النخبة للتجارة المحدودة','تعرف على شركة أوتاد النخبة للتجارة المحدودة في ود مدني: قصتنا ورؤيتنا وقيمنا وفريق العمل ومناطق التغطية.'),
           sectors=('قطاعات العمل | أوتاد النخبة للتجارة','الأعلاف، مدخلات صناعة الأعلاف، الأدوية البيطرية، الأدوية الزراعية، الإنتاج الحيواني والزراعي، والاستيراد والتصدير.'),
           products=('المنتجات | أعلاف ومدخلات وأدوية بيطرية | أوتاد النخبة','أعلاف دواجن (بادئ، نامي، ناهي)، علف تسمين الماشية، لايسين، مركزات بروتينية، بريمكس، مضادات حيوية بيطرية، مبيدات وأسمدة.'),
           quality=('الجودة | أوتاد النخبة للتجارة','التزام أوتاد النخبة بالجودة: ضمان الجودة والفحص والتوثيق والتتبع والرقابة من الاستلام حتى التسليم.'),
           partners=('الشراكات | كن شريكاً لأوتاد النخبة','فرص الشراكة مع أوتاد النخبة: موردو الأعلاف والأدوية البيطرية، الموزعون المعتمدون، والشراكات الاستراتيجية.'),
           contact=('تواصل معنا | أوتاد النخبة للتجارة',f'تواصل مع أوتاد النخبة في ود مدني على {PHONE_TXT} أو واتساب أو {EMAIL}. اطلب عرض سعر الآن.')),
'en': dict(index=('Awtad Alnokhbah Trading | Feed, Veterinary & Agrochemicals in Sudan','Awtad Alnokhbah Trading Co. Ltd in Wad Madani: poultry and cattle feed, feed manufacturing inputs, veterinary medicines, pesticides and fertilizers, import and export. 500+ clients.'),
           about=('About Us | Awtad Alnokhbah Trading Co. Ltd','About Awtad Alnokhbah Trading Co. Ltd in Wad Madani, Sudan: our story, vision, values, team and coverage.'),
           sectors=('Business Sectors | Awtad Alnokhbah Trading','Animal feed, feed inputs, veterinary medicines, agrochemicals, livestock and agricultural production, plus import and export.'),
           products=('Products | Feed, Inputs & Veterinary | Awtad Alnokhbah','Poultry starter, grower and finisher feed, cattle fattening feed, lysine, protein concentrates, premix, veterinary antibiotics, pesticides and fertilizers.'),
           quality=('Quality | Awtad Alnokhbah Trading','Our quality commitment: assurance, inspection, documentation, traceability and control from receipt to delivery.'),
           partners=('Partnerships | Partner with Awtad Alnokhbah','Partnership opportunities: feed and veterinary suppliers, authorised distributors and strategic partnerships.'),
           contact=('Contact | Awtad Alnokhbah Trading',f'Contact Awtad Alnokhbah in Wad Madani on {PHONE_TXT}, WhatsApp or {EMAIL}. Request a quote today.')),
}

def write(rel_file, html):
    p=OUT+rel_file; os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w',encoding='utf-8').write(html)

PAGES=[('index','','index.html',home),('about','about','about.html',about_page),('sectors','sectors','sectors.html',sectors_page),
       ('products','products','products.html',products_page),('quality','quality','quality.html',quality_page),
       ('partners','partners','partners.html',partners_page),('contact','contact','contact.html',contact_page)]
for lang in ('ar','en'):
    pre='' if lang=='ar' else 'en/'
    for key,rel,fn,fnc in PAGES:
        tt,dd=TITLES[lang][key]; write(pre+fn, page(lang,key,rel,tt,dd,fnc(lang)))
write('404.html', page('ar','404','404','الصفحة غير موجودة | أوتاد النخبة','الصفحة غير موجودة.',notfound('ar'),noindex=True))

items=''
for key,rel,fn,fnc in PAGES:
    for lang in ('ar','en'):
        items+=(f'<url><loc>{DOMAIN}{P(lang,rel)}</loc><lastmod>2026-10-11</lastmod>'
                f'<xhtml:link rel="alternate" hreflang="ar" href="{DOMAIN}{P("ar",rel)}"/>'
                f'<xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}{P("en",rel)}"/></url>')
open(OUT+'sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'+items+'</urlset>\n')
open(OUT+'robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
open(OUT+'_redirects','w').write('/team /about 301\n/en/team /en/about 301\n/articles / 301\n/articles/* / 301\n/en/articles /en/ 301\n/terms / 301\n/en/terms /en/ 301\n')
open(OUT+'_headers','w').write('''/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
/assets/*
  Cache-Control: public, max-age=604800
''')
open(OUT+'assets/site.js','w',encoding='utf-8').write(r"""(function(){
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
""")
print('built')

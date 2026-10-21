# موقع شركة أوتاد النخبة للتجارة المحدودة — awtad-trade.com

موقع ثابت (HTML) يعمل على Cloudflare Workers. أي تعديل يُرفع إلى GitHub يُنشر تلقائياً خلال دقيقة.

## الصفحات

| الصفحة | العربية | الإنجليزية |
|---|---|---|
| الرئيسية | public/index.html | public/en/index.html |
| من نحن | public/about.html | public/en/about.html |
| قطاعاتنا | public/sectors.html | public/en/sectors.html |
| المنتجات | public/products.html | public/en/products.html |
| الجودة | public/quality.html | public/en/quality.html |
| الشراكات | public/partners.html | public/en/partners.html |
| تواصل معنا | public/contact.html | public/en/contact.html |

- الصور: public/assets/img
- التنسيق: public/assets/style.css
- النماذج ترسل الطلب عبر واتساب إلى +249 91 234 0786

## تعديل نص بسيط
1. افتح الملف في GitHub واضغط أيقونة القلم (Edit).
2. عدّل النص، ثم اضغط **Commit changes**.
3. انتظر دقيقة وحدّث الموقع.

## لوحة الإدارة (awtad-trade.com/admin)

- **الدخول:** بكلمة المرور المحفوظة في Cloudflare باسم `ADMIN_PASSWORD` (Workers → awtad → Settings → Variables and Secrets).
- **الوظائف:** إضافة وظيفة وتعديلها ونشرها أو إغلاقها. تظهر في `/careers`، وتُغلق تلقائياً بعد آخر موعد للتقديم.
- **طلبات التوظيف:** تُحفظ مع السيرة الذاتية في مخزن Cloudflare KV باسم `awtad-data`. يصل إشعار إلى hr@ إذا أُضيف `RESEND_API_KEY`.
- **صور الموقع:** استبدال أي صورة واستعادة الأصل.
- **الألوان:** تغيير ألوان الموقع الأساسية.
- **روابط التواصل:** فيسبوك وإنستغرام وإكس وتيك توك ولينكدإن، وتظهر في ذيل الموقع وصفحة التواصل.

الملفات التقنية: `src/worker.js` (الخادم)، و`public/admin.html` (اللوحة)، و`public/assets/careers.js` (نموذج التقديم).

# Dispatcher_proje
MİKROSERVİS  TABANLI DİSPATCHER(API GATEWAY) SİSTEMİ

231307039- Sertaç Özdemir
231307069- Fatma Nilay Süzer
# 1.GİRİŞ

Bu projede,mikroservis mimarisi kullanılarak kullanıcı ve ürün işlemlerini yöneten bir sistem geliştirdik.Sistem, tüm istemci isteklerini tek bir noktadan karşılayan bir Dispatcher(API Gateway) uzerinden çalışmaktadır.Bu yapı sayesinde servisler birbirinden bağımsız hale (network isolation) gelmiştir.Bu projede amaçladığımız şey de buydu.

# 2.AMAÇ #
Bu projenin amacı:
-Mikroservis mimarisini uygulamak
-Dispatcher mantığını kurmak
-Servisler arası iletişimi sağlamak
-Kimlik doğrulama (Authentication) mekanızmasını sağlamak
-Mongo veri tabanı kullanmak
-Docker ile sistemi tek komutta bütün mikroservisler ve dispatcher çalışacak şekilde tasarlamak.
-Yük testi(k6) ve loglar ile sistemi gözlemlemek

# 3.Sistem Mimarisi
Sistem aşağıdaki bileşenlerden oluşmaktadır:
- Dispatcher
- Auth Service
- User Service
- Product Service
- MongoDB(User,Product database)
- Docker.

- Sistem mimarisi diyagramı
<img width="1670" height="603" alt="mermaid-diagram (1)" src="https://github.com/user-attachments/assets/f0d8a198-afea-449b-a80c-032942a9426c" />

# 4.Mikroservisler ve Görevleri

   4.1 Dispatcher(API Gateway)
  
  -Sistemin giriş noktasıdır
  
  -Gelen istekleri karşılar
  
  -Authorization(token kontrol) yapar.
  
  -İstekleri ilgili servislere yönlendirir
  
  -Log tutar.
  
  4.2 Auth Service
  
  -Token doğrulama işlemini gerçekleştirir
  
  -Dispatcherdan gelen tokenları kontrol eder
  
  -Geçerli token için 200 geçersiz için 401 döner
  
  4.3 User Service
  
  -Kullanıcı Oluşturma (POST)
  
  -Kullanıcı sorgulama(GET)
  
  -MongoDB üzerinde veri saklama
  
  4.4 Product Service
  
  -Ürün oluşturma (POST)
  
  -Ürün sorgulama (GET)
  
  -MongoDB üzerinde veri saklama
  
  # 5.Veritabanı yapısı
  
  -Projede NoSQL Veritabanı olarak MongoDB kullandık.
  
  user_service -> user_db
  
  product_service -> product_db
  
  Her mikroservis kendi veri tabanına sahiptir. Bu sayede servisler birbirinden bağımsızdır ve veri izolasyonu sağlanmıştır.
  
  # 6. Docker ve Ağ Yapısı

  Sistemde tüm servisler Docker container olarak çalıştırılmıştır.

  -Dispatcher dış dünyaya açıktır (port 8000)
  
  -Diğer servisler internal network üzerinden erişilir
  
  -docker-compose ile tüm yapı orkestre edilmiştir
  
  -Servisler micro_net ağı üzerinden haberleşmektedir
  
  # 7. Richardson Maturity Model (RMM)

  -Geliştirilen sistem RMM Level 2 seviyesindedir.
  
  -Kaynak tabanlı endpoint yapısı vardır (/users, /products)
  -HTTP metodları doğru kullanılmıştır (GET, POST)

  # 8. Trafik İzleme ve Loglama

  -Dispatcher servisinde tüm istekler loglanmıştır.

  Loglarda:

  -HTTP metodu
  -Endpoint bilgisi
  -İstek gövdesi (body)
  -Yönlendirilen servis adresi
  -Dönen HTTP durum kodu

  kayıt altına alınmıştır.

Bu sayede sistem trafiği analiz edilmiş ve servisler arası iletişim doğrulanmıştır.

# 9. Yük Testi (Performance Test)

Sistem performansı k6 aracı ile test edilmiştir.

Test sırasında:

10 → 50 → 100 sanal kullanıcı (VUs) kullanılmıştır

Dispatcher üzerinden User ve Product servislerine istek atılmıştır

Test Sonuçları:

Hata oranı: %0

Ortalama yanıt süresi: ~327 ms

yüzdelik dilim: ~921 ms

Tüm istekler başarıyla tamamlanmıştır

Bu sonuçlar sistemin yüksek yük altında stabil çalıştığını göstermektedir.
API Arayüzü
<img width="1891" height="956" alt="API Arayüzü" src="https://github.com/user-attachments/assets/274f45e3-2909-454d-bee7-1233694930e2" />

Loglar
<img width="1126" height="360" alt="log görüntü" src="https://github.com/user-attachments/assets/dda9956d-19aa-4f66-a9e4-a11e3e64d986" />

K6 Yük testi sonucu

<img width="1127" height="912" alt="k6 görüntü tamam" src="https://github.com/user-attachments/assets/05eafcf4-2b78-4cc7-9b42-c95c89949209" />

Mermaid kullanarak akış diyagramı
<img width="1244" height="2532" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/ad197735-edd5-44c3-b9cd-7376a83bcd03" />


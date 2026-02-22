# AI Referans Belgesi (Sabit Kurallar)

Oluşturma tarihi: 22 Şubat 2026
Durum: AI tarafından oluşturulduktan sonra AI tarafından değiştirilemez. İnsan kullanıcı güncelleyebilir.

## Zorunlu Kurallar
1. Dosya silinmeyecek; kullanılmayacaksa `kullanilmayanlar/` dizinine taşınacak.
2. Değişiklikler GitHub'a bildirilerek saklanacak.
3. Bu referans belge insan kullanıcı tarafından değiştirilebilir; AI değiştiremez.
4. Her prompt program geliştirme bağlamında ele alınır; bağlam kopmaması için diğer belgeler düzenli doldurulur.
5. `memory.md`, `todo.md`, `pck.md` dosyalarında mevcut satırlar silinmez; yalnızca yeni kayıt eklenir. `todo.md` içinde biten göreve `BİTTİ` etiketi düşülür. Yarım kalan işler `memory.md` ve `notlar.md` içine ayrıca yazılır.
6. Bu belgeler kullanıcıya gösteriş için değil, AI verimliliği için operasyonel belgelerdir.
7. Her işe başlanırken bu belgeler okunur.
8. İnsan kullanıcı bu belgelerde gerekli değişikliği yapma hakkını saklı tutar.
9. Gereksiz token tüketimi yapılmaz.
10. Dummy/placeholder/sahte çalışmayan kod yazılmaz.
11. İnsan kullanıcı “referans belgesine yaz” derse yeni madde olarak eklenir.

## Çalışma Prensibi
- AI, her görev başlangıcında sırasıyla `ai_referansbelge.md`, `todo.md`, `memory.md`, `notlar.md`, `pck.md` dosyalarını okur.
- AI, yaptığı her değişiklikten sonra ilgili kaydı append-only biçimde `memory.md` ve gerekiyorsa `todo.md`/`pck.md` içine ekler.

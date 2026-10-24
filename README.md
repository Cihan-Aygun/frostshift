# FrostShift — Inventory Lab

[English](#english) · [Türkçe](#türkçe)

## English

A synthetic seven-day inventory simulation: six stores, three frozen-product categories and three replenishment policies. Does moving stock between stores justify its transport cost?

### Run

Python 3.11+, standard library only:

```bash
python3 -m frostshift
```

Open http://127.0.0.1:8002. Use `--port 8012` if needed. Change coastal demand uplift, shipment fee and random seed. Select a day to inspect transfer routes and end-of-day stocks. The dashboard is in Turkish.

### Policies and assumptions

- **None:** sell available inventory without replenishment.
- **Depot:** replenish each SKU to two forecast days, subject to store capacity. Unlimited depot stock; each SKU shipment costs a fixed fee plus 3 TRY/carton.
- **Transfer:** visit products in fixed order, recipients by shortage and donors by distance. Target two forecast days; donor must retain three forecast days. Maximum 50 transferred cartons per day across all stores. Each SKU shipment costs a fixed fee + twice synthetic distance + 1 TRY/carton. Transfer only if quantity × 18 exceeds shipment cost.

Initial stock is 22 cartons/SKU at the two coastal stores and 65 elsewhere. Capacity is 240 cartons/store. Forecast daily demand is 8, 10 or 12 cartons/SKU by store, increased at coastal stores by the selected uplift. Actual daily demand is rounded, nonnegative Gaussian demand with standard deviation 2; all policies use identical draws. The forecast does not observe realized future demand.

Actions happen before daily sales; transport is refrigerated and arrives within the same day. No lead-time, temperature, expiry, road, handling or food-safety model. Transfers may reduce donor sales later. The heuristic is not globally optimal and the economic gate is not proof of realized benefit. Product order can affect allocation under the shared daily capacity.

Contribution = sold cartons × illustrative 18 TRY contribution/carton − logistics. It is not net profit. Inventory purchase cost, capital, waste and other expenses are excluded. The depot has external supply while transfers conserve existing stock; compare availability as well as contribution.

### Uncertainty and checks

The panel repeats the model for seeds 0–99 and reports transfer-minus-none contribution: mean, sorted-sample P10/P90 and positive share. These are synthetic sensitivity results, not calibrated real-world probabilities.

```bash
python3 -m unittest discover -s tests -v
```

Tests verify stock conservation, nonnegativity, store and daily transfer capacities over ten seeds, common demand, repeatability and the economic gate. API: `/api/scenario?seed=42&heat=25&fee=35`.

No Magnum affiliation or proprietary data. This is an independent educational prototype. Next steps: travel lead times, expiry batches, estimated demand distributions, explicit SKU handling costs and exact optimization benchmarks.

## Türkçe

Altı mağaza, üç dondurulmuş ürün kategorisi ve yedi gün için stok dengeleme simülasyonu. Amaç: **Mağazalar arası transfer taşıma maliyetine değer mi?**

### Kurulum

Python 3.11+ yeterli; ek paket veya API anahtarı gerekmez.

```bash
python3 -m frostshift
```

http://127.0.0.1:8002 adresini açın. Alternatif port: `python3 -m frostshift --port 8012`. Talep artışını, gönderi ücretini ve rastgelelik tohumunu değiştirin; gün seçerek transferleri ve gün sonu stoklarını inceleyin.

### Karar kuralları

- **Müdahale yok:** Mevcut stok satılır, yenileme yapılmaz.
- **Depodan tamamla:** Ürün başına iki tahmin gününe kadar stok eklenir. Depo sınırsızdır; her ürün gönderisi sabit ücret + kutu başına ₺3 tutar.
- **Mağazalar arası:** Ürün sırası sabittir; alıcılar eksik stoğa, göndericiler mesafeye göre sıralanır. Alıcı için iki günlük hedef, gönderici için üç günlük rezerv kullanılır. Günlük toplam taşıma kapasitesi 50 kutudur. Ürün gönderisi sabit ücret + sentetik mesafenin iki katı + kutu başına ₺1 tutar. Yalnızca kutu sayısı × ₺18 maliyeti aşıyorsa transfer yapılır.

İki sahil mağazası ürün başına 22, diğerleri 65 kutuyla başlar. Mağaza kapasitesi toplam 240 kutudur. Günlük temel talep ürün başına mağazaya göre 8, 10 veya 12 kutudur; sahilde seçilen artış uygulanır. Gerçekleşen talep, standart sapması 2 olan normal dağılımdan örneklenir, yuvarlanır ve sıfırın altına düşmez. Politikalar aynı talebi görür; kararlar gelecekte gerçekleşecek talebi bilmez.

Transferler satıştan önce, soğutmalı araçla aynı gün tamamlanır varsayılır. Yol süresi, sıcaklık, raf ömrü ve gıda güvenliği hesaplanmaz. Göndericinin ileride stok sıkıntısı yaşaması mümkündür. Sezgisel yöntem optimum garantisi vermez; ekonomik eşik de gerçekleşen kazancı garanti etmez. Günlük kapasite nedeniyle ürün sırası sonucu etkileyebilir.

**Katkı = satış × varsayımsal ₺18 − lojistik maliyeti.** Net kâr değildir. Ürün alım maliyeti, sermaye, atık ve diğer giderler dahil değildir. Depodan tamamlama dışarıdan yeni stok getirir; transfer ise toplam stoğu korur. Bu nedenle satış ve stok kullanılabilirliği de karşılaştırılmalıdır.

### Belirsizlik ve doğrulama

Panel 0–99 tohumlarıyla 100 senaryoyu tekrarlar. Transferin müdahalesiz plana göre katkı farkının ortalamasını, P10/P90 değerlerini ve pozitif sonuç oranını gösterir. Bunlar sentetik duyarlılık sonuçlarıdır; gerçek başarı olasılığı değildir.

```bash
python3 -m unittest discover -s tests -v
```

Testler stok korunumu, negatif olmayan stoklar, mağaza ve taşıma kapasitesi, eşit talep, tekrarlanabilirlik ve ekonomik eşiği denetler. API: `/api/scenario?seed=42&heat=25&fee=35`.

Magnum ile resmî bağlantı veya şirkete ait veri yoktur. Bağımsız eğitim prototipidir. Sonraki çalışmalar: teslimat süreleri, parti bazında raf ömrü, veriyle tahmin edilen talep ve kesin optimizasyon karşılaştırması.
